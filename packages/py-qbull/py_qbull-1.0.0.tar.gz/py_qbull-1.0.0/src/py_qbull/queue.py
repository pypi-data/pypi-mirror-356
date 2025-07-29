"""
Queue class for managing job queues with Redis backend.

This module provides the Queue class which supports priorities, rate limiting,
job groups, and event subscriptions for robust job queue management.
"""

import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
import redis
import redis.asyncio as aioredis

from .types import (
    QueueOptions, JobOptions, JobCallbacks, QueueStatus, 
    WorkerInfo, JobData, RateLimitOptions
)
from .errors import RateLimitError, QueueError, JobNotFoundError


class Queue:
    """
    Queue class for managing job queues with Redis backend.
    
    Supports priorities, rate limiting, job groups, and event subscriptions.
    Designed to be non-blocking and work in both synchronous and asynchronous contexts.
    """
    
    def __init__(self, app_name: str, queue_name: str, options: QueueOptions):
        """
        Initialize a new Queue instance.
        
        Args:
            app_name: Application name for namespacing
            queue_name: Queue name for identification  
            options: Queue configuration options
        """
        self.connection = options.connection
        self.app_name = app_name
        self.queue_name = queue_name
        self.prefix = f"{app_name}:{queue_name}"
        
        # Initialize Redis keys for different job states
        self.failed_set = f"{self.prefix}:failed"
        self.completed_set = f"{self.prefix}:completed"
        self.delayed_set = f"{self.prefix}:delayed"
        self.events_key = f"{self.prefix}:events"
        self.counter_key = f"{self.prefix}:counter"
        self.groups_set_key = f"{self.prefix}:groups:set"
        
        # Initialize priority queue prefix
        self.priority_prefix = f"{self.prefix}:priority"
        
        # Initialize rate limiting configuration
        self.rate_limit_key = f"{self.prefix}:ratelimit"
        self.default_rate_limit = options.rate_limit or RateLimitOptions()
        
        # Load Lua scripts
        self._load_lua_scripts()
        
        # Initialize job subscription tracking
        self.job_subscriptions: Dict[str, JobCallbacks] = {}
    
    def _load_lua_scripts(self):
        """Load Lua scripts for atomic operations."""
        scripts_dir = Path(__file__).parent / "lua_scripts"
        
        try:
            with open(scripts_dir / "add_job.lua", "r") as f:
                self.add_job_script = f.read()
            with open(scripts_dir / "retry_job.lua", "r") as f:
                self.retry_job_script = f.read()
        except FileNotFoundError as e:
            raise QueueError(
                f"Could not load Lua scripts: {e}",
                queue_name=self.queue_name,
                app_name=self.app_name
            )
    
    @staticmethod
    async def flush_all(connection: redis.Redis) -> None:
        """
        Clean the entire Redis database.
        
        Args:
            connection: Redis connection instance
            
        Raises:
            QueueError: If connection is invalid
        """
        if not connection:
            raise QueueError("A valid Redis connection is required")
        
        if isinstance(connection, aioredis.Redis):
            await connection.flushall()
        else:
            connection.flushall()
        
        print("Redis database cleaned completely")
    
    async def add(
        self, 
        job_name: str, 
        data: Any, 
        options: Optional[JobOptions] = None
    ) -> str:
        """
        Add a job to the queue with priority support.
        
        Args:
            job_name: Name of the job
            data: Job data payload
            options: Job configuration options
            
        Returns:
            Job ID string
            
        Raises:
            RateLimitError: If rate limit is exceeded
            QueueError: If job addition fails
        """
        if options is None:
            options = JobOptions()
        
        # Check global rate limit
        is_limited, ttl = await self._is_rate_limited()
        if is_limited:
            raise RateLimitError(
                f"Rate limit reached. Try again in {ttl}ms",
                retry_after=ttl,
                limit_type="global"
            )
        
        # Check group rate limit if applicable
        group = data.get("group", {}).get("id", "default") if isinstance(data, dict) else "default"
        if group != "default":
            is_group_limited, group_ttl = await self._is_rate_limited(group)
            if is_group_limited:
                raise RateLimitError(
                    f"Group rate limit reached. Try again in {group_ttl}ms",
                    retry_after=group_ttl,
                    limit_type="group",
                    group_id=group
                )
        
        timestamp = int(time.time() * 1000)  # milliseconds
        priority = options.priority or 0
        
        # Prepare job options for serialization
        job_options_dict = {
            "attempts": options.attempts,
            "backoff": {
                "type": options.backoff.type.value,
                "delay": options.backoff.delay,
                "max_delay": options.backoff.max_delay,
                "jitter": options.backoff.jitter
            } if options.backoff else None,
            "remove_on_complete": options.remove_on_complete,
            "remove_on_fail": options.remove_on_fail,
            "priority": priority,
            "delay": options.delay,
            "job_id": options.job_id
        }
        
        # Define Redis keys for the Lua script
        keys = [
            f"{self.prefix}:wait",  # wait_key
            f"{self.prefix}:meta",  # meta_key  
            self.counter_key,       # counter_key
            self.events_key,        # events_key
            f"{self.prefix}:groups:{group}",  # group_key
            self.groups_set_key,    # groups_set_key
            self.delayed_set,       # delayed_key
            f"{self.priority_prefix}:{group}"  # priority_key
        ]
        
        args = [
            job_name,
            json.dumps(data),
            json.dumps(job_options_dict),
            str(timestamp),
            self.prefix,
            group,
            str(priority)
        ]
        
        try:
            if isinstance(self.connection, aioredis.Redis):
                job_id = await self.connection.eval(self.add_job_script, len(keys), *keys, *args)
            else:
                job_id = self.connection.eval(self.add_job_script, len(keys), *keys, *args)
            
            return str(job_id)
            
        except Exception as error:
            raise QueueError(
                f"Error adding job: {error}",
                queue_name=self.queue_name,
                app_name=self.app_name
            )
    
    async def get_job(self, job_id: str) -> Optional[JobData]:
        """
        Retrieve job information by ID.
        
        Args:
            job_id: The job identifier
            
        Returns:
            JobData instance or None if not found
        """
        job_key = f"{self.prefix}:job:{job_id}"
        
        try:
            if isinstance(self.connection, aioredis.Redis):
                job_data = await self.connection.hgetall(job_key)
            else:
                job_data = self.connection.hgetall(job_key)
            
            if not job_data:
                return None
            
            # Convert bytes to strings if needed (for sync Redis)
            if isinstance(list(job_data.keys())[0], bytes):
                job_data = {k.decode(): v.decode() for k, v in job_data.items()}
            
            # Parse job data
            return JobData(
                id=job_data["id"],
                name=job_data["name"],
                data=json.loads(job_data["data"]),
                options=JobOptions(**json.loads(job_data["options"])),
                timestamp=int(job_data["timestamp"]),
                attempts_made=int(job_data.get("attempts_made", 0)),
                processed_on=int(job_data["processed_on"]) if job_data.get("processed_on") else None,
                finished_on=int(job_data["finished_on"]) if job_data.get("finished_on") else None,
                failed_reason=job_data.get("failed_reason"),
                group=job_data.get("group", "default"),
                status=job_data.get("status", "waiting")
            )
            
        except Exception as error:
            raise QueueError(
                f"Error retrieving job {job_id}: {error}",
                queue_name=self.queue_name,
                app_name=self.app_name
            )
    
    async def get_status(self) -> QueueStatus:
        """
        Get current queue status including job counts and worker information.
        
        Returns:
            QueueStatus with current queue state
        """
        try:
            # Get job counts from different sets/lists
            if isinstance(self.connection, aioredis.Redis):
                # Async version
                pipe = self.connection.pipeline()
                
                # Count jobs in different states
                pipe.scard(self.failed_set)
                pipe.scard(self.completed_set)
                pipe.zcard(self.delayed_set)
                pipe.smembers(self.groups_set_key)
                
                results = await pipe.execute()
                failed_count = results[0]
                completed_count = results[1] 
                delayed_count = results[2]
                groups = results[3]
                
                # Count waiting and processing jobs
                waiting_count = 0
                processing_count = 0
                
                for group in groups:
                    group_key = f"{self.prefix}:groups:{group}"
                    priority_key = f"{self.priority_prefix}:{group}"
                    processing_key = f"{self.prefix}:processing:{group}"
                    
                    pipe.llen(group_key)
                    pipe.zcard(priority_key)
                    pipe.scard(processing_key)
                
                if groups:
                    group_results = await pipe.execute()
                    for i in range(0, len(group_results), 3):
                        waiting_count += group_results[i] + group_results[i + 1]
                        processing_count += group_results[i + 2]
                
            else:
                # Sync version
                failed_count = self.connection.scard(self.failed_set)
                completed_count = self.connection.scard(self.completed_set)
                delayed_count = self.connection.zcard(self.delayed_set)
                groups = self.connection.smembers(self.groups_set_key)
                
                waiting_count = 0
                processing_count = 0
                
                for group in groups:
                    if isinstance(group, bytes):
                        group = group.decode()
                    
                    group_key = f"{self.prefix}:groups:{group}"
                    priority_key = f"{self.priority_prefix}:{group}"
                    processing_key = f"{self.prefix}:processing:{group}"
                    
                    waiting_count += self.connection.llen(group_key)
                    waiting_count += self.connection.zcard(priority_key)
                    processing_count += self.connection.scard(processing_key)
            
            # Get worker information (simplified for now)
            workers: List[WorkerInfo] = []
            active_workers = 0
            total_workers = 0
            
            return QueueStatus(
                waiting=waiting_count,
                processing=processing_count,
                completed=completed_count,
                failed=failed_count,
                delayed=delayed_count,
                total_workers=total_workers,
                active_workers=active_workers,
                workers=workers
            )
            
        except Exception as error:
            raise QueueError(
                f"Error getting queue status: {error}",
                queue_name=self.queue_name,
                app_name=self.app_name
            )
    
    async def retry_job(self, job_id: str) -> bool:
        """
        Retry a specific job.
        
        Args:
            job_id: Job identifier to retry
            
        Returns:
            True if job was retried successfully
            
        Raises:
            JobNotFoundError: If job doesn't exist
            QueueError: If retry fails
        """
        job = await self.get_job(job_id)
        if not job:
            raise JobNotFoundError(job_id)
        
        if job.status != "failed":
            raise QueueError(
                f"Job {job_id} is not in failed state",
                queue_name=self.queue_name,
                app_name=self.app_name
            )
        
        # Calculate retry delay using backoff strategy
        delay = self._calculate_backoff(job.attempts_made + 1, job.options.backoff)
        
        keys = [
            f"{self.prefix}:job:{job_id}",  # job_key
            f"{self.prefix}:groups:{job.group}",  # group_key
            f"{self.priority_prefix}:{job.group}",  # priority_key
            self.failed_set,  # failed_key
            self.delayed_set,  # delayed_key
            self.events_key   # events_key
        ]
        
        args = [
            job_id,
            str(int(time.time() * 1000)),
            str(delay),
            str(job.options.attempts)
        ]
        
        try:
            if isinstance(self.connection, aioredis.Redis):
                result = await self.connection.eval(self.retry_job_script, len(keys), *keys, *args)
            else:
                result = self.connection.eval(self.retry_job_script, len(keys), *keys, *args)
            
            success, message = result
            if not success:
                raise QueueError(
                    f"Failed to retry job {job_id}: {message}",
                    queue_name=self.queue_name,
                    app_name=self.app_name
                )
            
            return True
            
        except Exception as error:
            raise QueueError(
                f"Error retrying job {job_id}: {error}",
                queue_name=self.queue_name,
                app_name=self.app_name
            )
    
    async def _is_rate_limited(self, group: Optional[str] = None) -> tuple[bool, int]:
        """
        Check if rate limit is exceeded.
        
        Args:
            group: Optional group to check rate limit for
            
        Returns:
            Tuple of (is_limited, ttl_ms)
        """
        rate_limit = self.default_rate_limit
        if rate_limit.max <= 0:
            return False, 0
        
        key = f"{self.rate_limit_key}:{group}" if group else self.rate_limit_key
        current_time = int(time.time() * 1000)
        window_start = current_time - rate_limit.duration
        
        try:
            if isinstance(self.connection, aioredis.Redis):
                pipe = self.connection.pipeline()
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.expire(key, rate_limit.duration // 1000 + 1)
                results = await pipe.execute()
                current_count = results[1]
            else:
                pipe = self.connection.pipeline()
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.expire(key, rate_limit.duration // 1000 + 1)
                results = pipe.execute()
                current_count = results[1]
            
            if current_count >= rate_limit.max:
                # Get oldest entry to calculate TTL
                if isinstance(self.connection, aioredis.Redis):
                    oldest = await self.connection.zrange(key, 0, 0, withscores=True)
                else:
                    oldest = self.connection.zrange(key, 0, 0, withscores=True)
                
                if oldest:
                    ttl = int(oldest[0][1] + rate_limit.duration - current_time)
                    return True, max(0, ttl)
            
            return False, 0
            
        except Exception:
            # If rate limiting fails, allow the operation
            return False, 0
    
    def _calculate_backoff(self, attempt: int, backoff_options) -> int:
        """
        Calculate backoff delay for retry attempts.
        
        Args:
            attempt: Current attempt number
            backoff_options: Backoff configuration
            
        Returns:
            Delay in milliseconds
        """
        if not backoff_options:
            return 1000  # Default 1 second
        
        if backoff_options.strategy:
            return backoff_options.strategy(attempt, None, None)
        
        if backoff_options.type.value == "fixed":
            delay = backoff_options.delay
        elif backoff_options.type.value == "linear":
            delay = backoff_options.delay * attempt
        else:  # exponential
            delay = backoff_options.delay * (2 ** (attempt - 1))
        
        # Apply jitter if configured
        if backoff_options.jitter:
            import random
            if isinstance(backoff_options.jitter, bool):
                jitter_amount = delay * 0.1  # 10% jitter
            else:
                jitter_amount = backoff_options.jitter
            
            delay += random.randint(-int(jitter_amount), int(jitter_amount))
        
        return min(delay, backoff_options.max_delay) 