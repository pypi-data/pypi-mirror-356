"""
Worker class for processing jobs from Redis queues.

This module provides the Worker class which supports job groups, concurrency control,
retries, stall recovery, and round-robin processing. Designed to be non-blocking
and work efficiently in Kubernetes pod environments.
"""

import asyncio
import json
import time
import uuid
import os
import socket
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Callable
import redis
import redis.asyncio as aioredis
from datetime import datetime

from .types import (
    WorkerOptions, JobData, JobProcessor, BackoffStrategy,
    JobCompletedEvent, JobFailedEvent, JobStalledEvent, 
    JobRetriesExhaustedEvent, JobOptions, BackoffOptions
)
from .errors import WorkerError, UnrecoverableError, RateLimitError


class Worker:
    """
    Worker class for processing jobs from Redis queues.
    
    Supports job groups, concurrency control, retries, and stall recovery.
    Uses round-robin scheduling for fair group processing and is designed
    to work efficiently in distributed environments like Kubernetes.
    """
    
    def __init__(
        self, 
        app_name: str, 
        queue_name: str, 
        processor: JobProcessor, 
        options: WorkerOptions
    ):
        """
        Initialize a new Worker instance.
        
        Args:
            app_name: Application name for namespacing
            queue_name: Queue name for identification
            processor: Function to process jobs
            options: Worker configuration options
        """
        self.app_name = app_name
        self.queue_name = queue_name
        self.prefix = f"{app_name}:{queue_name}"
        self.processor = processor
        
        if not options.connection:
            raise WorkerError("A valid Redis connection is required")
        
        self.connection = options.connection
        
        # Initialize worker identification
        self.worker_id = str(uuid.uuid4())
        self.hostname = socket.gethostname()
        self.pid = os.getpid()
        self.started_at = datetime.now()
        
        # Initialize job tracking
        self.processing_jobs: Dict[str, str] = {}  # job_id -> token
        self.processing_by_group: Dict[str, Dict[str, str]] = {}  # group -> {job_id -> token}
        
        # Initialize group management with round-robin
        self.groups = options.groups or []
        self.groups_set_key = f"{self.prefix}:groups:set"
        self.current_group_idx = 0
        
        # Configuration options
        self.concurrency = options.concurrency
        self.group_concurrency = options.group_concurrency
        self.remove_on_complete = options.remove_on_complete
        self.remove_on_fail = options.remove_on_fail
        self.batch_size = options.batch_size
        self.poll_interval = options.poll_interval / 1000.0  # Convert to seconds
        self.stall_interval = options.stall_interval / 1000.0
        self.lock_duration = options.lock_duration
        self.max_stalled_count = options.max_stalled_count
        self.backoff = options.backoff
        self.heartbeat_interval = options.heartbeat_interval / 1000.0
        self.stalled_check_interval = options.stalled_check_interval / 1000.0
        self.stalled_timeout = options.stalled_timeout
        
        # Initialize Redis keys
        self.heartbeat_key = f"{self.prefix}:workers:{self.worker_id}"
        self.events_key = f"{self.prefix}:events"
        self.locks_key = f"{self.prefix}:locks"
        
        # Execution control
        self.is_running = False
        self._shutdown_event = asyncio.Event()
        
        # Background tasks
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._stalled_check_task: Optional[asyncio.Task] = None
        self._delayed_jobs_task: Optional[asyncio.Task] = None
        self._main_loop_task: Optional[asyncio.Task] = None
        
        # Load Lua scripts
        self._load_lua_scripts()
        
        # Initialize group processing maps
        for group in self.groups:
            self.processing_by_group[group] = {}
    
    def _load_lua_scripts(self):
        """Load Lua scripts for atomic operations."""
        scripts_dir = Path(__file__).parent / "lua_scripts"
        
        try:
            with open(scripts_dir / "get_jobs.lua", "r") as f:
                self.get_jobs_script = f.read()
        except FileNotFoundError:
            # Fallback to individual Redis calls if Lua scripts not available
            self.get_jobs_script = None
    
    async def start(self) -> None:
        """
        Start the worker to begin processing jobs.
        
        This method is non-blocking and starts all background tasks including:
        - Main job processing loop
        - Heartbeat maintenance
        - Stalled job recovery
        - Delayed job processing
        """
        if self.is_running:
            return
        
        self.is_running = True
        self._shutdown_event.clear()
        
        try:
            # Refresh groups from Redis
            await self._refresh_groups()
            
            # Start background tasks
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            self._stalled_check_task = asyncio.create_task(self._stalled_check_loop())
            self._delayed_jobs_task = asyncio.create_task(self._delayed_jobs_loop())
            self._main_loop_task = asyncio.create_task(self._main_processing_loop())
            
            print(f"🚀 Worker {self.worker_id} started with concurrency {self.concurrency}")
            
        except Exception as error:
            self.is_running = False
            raise WorkerError(
                f"Failed to start worker: {error}",
                worker_id=self.worker_id,
                operation="start"
            )
    
    async def stop(self, timeout_ms: int = 30000) -> None:
        """
        Stop the worker gracefully.
        
        Args:
            timeout_ms: Timeout in milliseconds to wait for graceful shutdown
        """
        if not self.is_running:
            return
        
        print(f"🛑 Stopping worker {self.worker_id}...")
        
        # Signal shutdown
        self.is_running = False
        self._shutdown_event.set()
        
        # Cancel background tasks
        tasks_to_cancel = [
            self._heartbeat_task,
            self._stalled_check_task, 
            self._delayed_jobs_task,
            self._main_loop_task
        ]
        
        for task in tasks_to_cancel:
            if task and not task.done():
                task.cancel()
        
        # Wait for tasks to complete with timeout
        timeout_seconds = timeout_ms / 1000.0
        try:
            await asyncio.wait_for(
                asyncio.gather(*[t for t in tasks_to_cancel if t], return_exceptions=True),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            print(f"⚠️ Worker {self.worker_id} shutdown timeout exceeded")
        
        # Release all locks for jobs being processed
        await self._release_all_locks()
        
        # Remove worker heartbeat
        try:
            if isinstance(self.connection, aioredis.Redis):
                await self.connection.delete(self.heartbeat_key)
            else:
                self.connection.delete(self.heartbeat_key)
        except Exception:
            pass  # Ignore cleanup errors
        
        print(f"✅ Worker {self.worker_id} stopped")
    
    async def _refresh_groups(self) -> None:
        """Refresh the list of job groups from Redis."""
        try:
            if isinstance(self.connection, aioredis.Redis):
                redis_groups = await self.connection.smembers(self.groups_set_key)
                redis_groups = [g.decode() if isinstance(g, bytes) else g for g in redis_groups]
            else:
                redis_groups = self.connection.smembers(self.groups_set_key)
                redis_groups = [g.decode() if isinstance(g, bytes) else g for g in redis_groups]
            
            # Merge configured groups with groups found in Redis
            all_groups = set(self.groups + redis_groups)
            if not all_groups:
                all_groups = {"default"}
            
            # Update groups and initialize processing maps
            new_groups = all_groups - set(self.groups)
            for group in new_groups:
                self.processing_by_group[group] = {}
            
            self.groups = list(all_groups)
            
        except Exception as error:
            print(f"⚠️ Error refreshing groups: {error}")
            # Fallback to default group if refresh fails
            if not self.groups:
                self.groups = ["default"]
                self.processing_by_group["default"] = {}
    
    async def _main_processing_loop(self) -> None:
        """
        Main job processing loop with round-robin group scheduling.
        
        This is the core of the worker that implements the round-robin algorithm
        to ensure fair processing across all job groups.
        """
        cycles_without_jobs = 0
        
        while self.is_running and not self._shutdown_event.is_set():
            try:
                found_jobs = False
                
                # Refresh groups periodically
                if cycles_without_jobs % 100 == 0:
                    await self._refresh_groups()
                
                # Process jobs from each group in round-robin fashion
                for _ in range(len(self.groups)):
                    if not self.is_running:
                        break
                    
                    # Check global concurrency limit
                    free_global = self.concurrency - len(self.processing_jobs)
                    if free_global <= 0:
                        await asyncio.sleep(0.01)  # Brief pause if at capacity
                        continue
                    
                    # Get current group using round-robin
                    current_group = self.groups[self.current_group_idx]
                    self.current_group_idx = (self.current_group_idx + 1) % len(self.groups)
                    
                    # Check group concurrency limit
                    group_processing = self.processing_by_group.get(current_group, {})
                    free_group = self.group_concurrency - len(group_processing)
                    if free_group <= 0:
                        continue  # Skip to next group immediately
                    
                    # Calculate batch size for this group
                    current_batch_size = min(
                        self.batch_size,
                        free_global,
                        free_group
                    )
                    
                    if current_batch_size <= 0:
                        continue
                    
                    # Get jobs from current group
                    jobs = await self._get_jobs_competitively(current_group, current_batch_size)
                    
                    if jobs:
                        found_jobs = True
                        # Process jobs concurrently
                        tasks = []
                        for job_id, job_type in jobs:
                            task = asyncio.create_task(
                                self._handle_job_with_token(job_id, current_group)
                            )
                            tasks.append(task)
                        
                        # Don't wait for completion - let jobs run in background
                        # This ensures non-blocking behavior
                
                # Adaptive polling: increase sleep time when no jobs found
                if not found_jobs:
                    cycles_without_jobs += 1
                    sleep_time = min(self.poll_interval * cycles_without_jobs, 1.0)
                    await asyncio.sleep(sleep_time)
                else:
                    cycles_without_jobs = 0
                    await asyncio.sleep(self.poll_interval)
                
            except Exception as error:
                print(f"❌ Error in main processing loop: {error}")
                await asyncio.sleep(1.0)  # Prevent tight error loops
    
    async def _get_jobs_competitively(self, group: str, batch_size: int) -> List[tuple[str, str]]:
        """
        Get jobs from a group using competitive acquisition.
        
        Args:
            group: Group name to get jobs from
            batch_size: Number of jobs to attempt to acquire
            
        Returns:
            List of (job_id, job_type) tuples
        """
        jobs = []
        
        if self.get_jobs_script:
            # Use Lua script for atomic job acquisition
            keys = [
                f"{self.prefix}:groups:{group}",  # group_key
                f"{self.prefix}:priority:{group}",  # priority_key  
                f"{self.prefix}:processing:{group}",  # processing_key
                self.locks_key  # lock_key
            ]
            
            args = [
                self.worker_id,
                str(int(time.time() * 1000)),
                str(self.lock_duration),
                str(batch_size)
            ]
            
            try:
                if isinstance(self.connection, aioredis.Redis):
                    result = await self.connection.eval(
                        self.get_jobs_script, len(keys), *keys, *args
                    )
                else:
                    result = self.connection.eval(
                        self.get_jobs_script, len(keys), *keys, *args
                    )
                
                # Handle both old format (job_id, job_type) and new format (job_id, job_type, token)
                for job_result in result:
                    if len(job_result) == 3:
                        # New format with token
                        job_id, job_type, token = job_result
                        self.processing_jobs[job_id] = token
                        jobs.append((job_id, job_type))
                    else:
                        # Old format without token (fallback)
                        job_id, job_type = job_result
                        jobs.append((job_id, job_type))
                
            except Exception as error:
                print(f"⚠️ Error using Lua script for job acquisition: {error}")
                # Fall back to individual Redis calls
        
        # Fallback: individual Redis calls (less efficient but more compatible)
        if not jobs:
            jobs = await self._get_jobs_individually(group, batch_size)
        
        return jobs
    
    async def _get_jobs_individually(self, group: str, batch_size: int) -> List[tuple[str, str]]:
        """
        Fallback method to get jobs using individual Redis calls.
        
        Args:
            group: Group name to get jobs from
            batch_size: Number of jobs to attempt to acquire
            
        Returns:
            List of (job_id, job_type) tuples
        """
        jobs = []
        group_key = f"{self.prefix}:groups:{group}"
        priority_key = f"{self.prefix}:priority:{group}"
        
        try:
            # Try priority queue first
            if isinstance(self.connection, aioredis.Redis):
                priority_count = await self.connection.zcard(priority_key)
            else:
                priority_count = self.connection.zcard(priority_key)
            
            if priority_count > 0:
                # Get high priority jobs
                priority_jobs_needed = min(batch_size, priority_count)
                
                for _ in range(priority_jobs_needed):
                    if isinstance(self.connection, aioredis.Redis):
                        job_id = await self.connection.zpopmax(priority_key, 1)
                    else:
                        job_id = self.connection.zpopmax(priority_key, 1)
                    
                    if job_id:
                        job_id = job_id[0][0]  # Extract job ID from score tuple
                        if isinstance(job_id, bytes):
                            job_id = job_id.decode()
                        
                        # Try to acquire lock
                        if await self._acquire_lock(job_id):
                            jobs.append((job_id, "priority"))
                            if len(jobs) >= batch_size:
                                break
                        else:
                            # Put job back if couldn't acquire lock
                            if isinstance(self.connection, aioredis.Redis):
                                await self.connection.zadd(priority_key, {job_id: -1})
                            else:
                                self.connection.zadd(priority_key, {job_id: -1})
            
            # Get remaining jobs from regular queue
            remaining_needed = batch_size - len(jobs)
            for _ in range(remaining_needed):
                if isinstance(self.connection, aioredis.Redis):
                    job_id = await self.connection.rpop(group_key)
                else:
                    job_id = self.connection.rpop(group_key)
                
                if not job_id:
                    break  # No more jobs
                
                if isinstance(job_id, bytes):
                    job_id = job_id.decode()
                
                # Try to acquire lock
                if await self._acquire_lock(job_id):
                    jobs.append((job_id, "regular"))
                else:
                    # Put job back if couldn't acquire lock
                    if isinstance(self.connection, aioredis.Redis):
                        await self.connection.rpush(group_key, job_id)
                    else:
                        self.connection.rpush(group_key, job_id)
        
        except Exception as error:
            print(f"⚠️ Error getting jobs individually: {error}")
        
        return jobs
    
    async def _acquire_lock(self, job_id: str) -> bool:
        """
        Acquire a distributed lock for a job.
        
        Args:
            job_id: Job identifier to lock
            
        Returns:
            True if lock was acquired successfully
        """
        lock_field = f"lock:{job_id}"
        current_time = int(time.time() * 1000)
        
        try:
            if isinstance(self.connection, aioredis.Redis):
                current_lock = await self.connection.hget(self.locks_key, lock_field)
            else:
                current_lock = self.connection.hget(self.locks_key, lock_field)
            
            if current_lock:
                lock_data = json.loads(current_lock.decode() if isinstance(current_lock, bytes) else current_lock)
                lock_expires = lock_data.get("expires", 0)
                
                # Check if lock is still valid
                if current_time < lock_expires:
                    return False  # Lock is still held by another worker
            
            # Acquire lock
            token = str(uuid.uuid4())
            lock_data = {
                "worker_id": self.worker_id,
                "acquired_at": current_time,
                "expires": current_time + self.lock_duration,
                "token": token
            }
            
            if isinstance(self.connection, aioredis.Redis):
                await self.connection.hset(self.locks_key, lock_field, json.dumps(lock_data))
            else:
                self.connection.hset(self.locks_key, lock_field, json.dumps(lock_data))
            
            # Track the lock
            self.processing_jobs[job_id] = token
            
            return True
            
        except Exception as error:
            print(f"⚠️ Error acquiring lock for job {job_id}: {error}")
            return False
    
    async def _release_lock(self, job_id: str, token: str) -> None:
        """
        Release a distributed lock for a job.
        
        Args:
            job_id: Job identifier
            token: Lock token for verification
        """
        lock_field = f"lock:{job_id}"
        
        try:
            if isinstance(self.connection, aioredis.Redis):
                current_lock = await self.connection.hget(self.locks_key, lock_field)
            else:
                current_lock = self.connection.hget(self.locks_key, lock_field)
            
            if current_lock:
                lock_data = json.loads(current_lock.decode() if isinstance(current_lock, bytes) else current_lock)
                
                # Only release if we own the lock
                if lock_data.get("token") == token and lock_data.get("worker_id") == self.worker_id:
                    if isinstance(self.connection, aioredis.Redis):
                        await self.connection.hdel(self.locks_key, lock_field)
                    else:
                        self.connection.hdel(self.locks_key, lock_field)
            
            # Remove from tracking
            self.processing_jobs.pop(job_id, None)
            
            # Remove from group tracking
            for group_jobs in self.processing_by_group.values():
                group_jobs.pop(job_id, None)
                
        except Exception as error:
            print(f"⚠️ Error releasing lock for job {job_id}: {error}")
    
    async def _release_all_locks(self) -> None:
        """Release all locks held by this worker."""
        jobs_to_release = list(self.processing_jobs.items())
        
        for job_id, token in jobs_to_release:
            await self._release_lock(job_id, token)
    
    async def _handle_job_with_token(self, job_id: str, group: str) -> None:
        """
        Handle job processing with lock token management.
        
        Args:
            job_id: Job identifier
            group: Job group name
        """
        token = self.processing_jobs.get(job_id)
        if not token:
            print(f"⚠️ No token found for job {job_id}")
            return
        
        # Add to group tracking
        if group not in self.processing_by_group:
            self.processing_by_group[group] = {}
        self.processing_by_group[group][job_id] = token
        
        try:
            await self._process_job(job_id)
        finally:
            # Always release lock when done
            await self._release_lock(job_id, token)
    
    async def _process_job(self, job_id: str) -> None:
        """
        Process a single job with error handling and retries.
        
        Args:
            job_id: Job identifier to process
        """
        start_time = time.time()
        job_key = f"{self.prefix}:job:{job_id}"
        
        try:
            # Get job data
            if isinstance(self.connection, aioredis.Redis):
                job_data = await self.connection.hgetall(job_key)
            else:
                job_data = self.connection.hgetall(job_key)
            
            if not job_data:
                print(f"⚠️ Job {job_id} not found")
                return
            
            # Convert bytes to strings if needed
            if isinstance(list(job_data.keys())[0], bytes):
                job_data = {k.decode(): v.decode() for k, v in job_data.items()}
            
            # Parse job data with proper type conversion
            options_dict = json.loads(job_data["options"])
            
            # Convert backoff dict to BackoffOptions if present
            if options_dict.get("backoff") and isinstance(options_dict["backoff"], dict):
                backoff_dict = options_dict["backoff"]
                from .types import BackoffOptions, BackoffStrategy
                options_dict["backoff"] = BackoffOptions(
                    type=BackoffStrategy(backoff_dict.get("type", "exponential")),
                    delay=backoff_dict.get("delay", 1000),
                    max_delay=backoff_dict.get("max_delay", 300000),
                    jitter=backoff_dict.get("jitter", False)
                )
            
            job = JobData(
                id=job_data["id"],
                name=job_data["name"],
                data=json.loads(job_data["data"]),
                options=JobOptions(**options_dict),
                timestamp=int(job_data["timestamp"]),
                attempts_made=int(job_data.get("attempts_made", 0)),
                group=job_data.get("group", "default"),
                status=job_data.get("status", "waiting")
            )
            
            # Update job status to processing
            processed_on = int(time.time() * 1000)
            if isinstance(self.connection, aioredis.Redis):
                await self.connection.hset(job_key, mapping={"status": "processing", "processed_on": str(processed_on)})
            else:
                self.connection.hset(job_key, mapping={"status": "processing", "processed_on": str(processed_on)})
            
            print(f"🔄 Processing job {job_id} ({job.name}) - attempt {job.attempts_made + 1}")
            
            # Process the job
            try:
                result = await self.processor(job)
                
                # Job completed successfully
                duration = int((time.time() - start_time) * 1000)
                finished_on = int(time.time() * 1000)
                
                # Update job status
                if isinstance(self.connection, aioredis.Redis):
                    await self.connection.hset(
                        job_key, 
                        mapping={
                            "status": "completed",
                            "finished_on": str(finished_on),
                            "result": json.dumps(result) if result is not None else ""
                        }
                    )
                else:
                    self.connection.hset(
                        job_key, 
                        mapping={
                            "status": "completed",
                            "finished_on": str(finished_on),
                            "result": json.dumps(result) if result is not None else ""
                        }
                    )
                
                # Handle job removal
                await self._handle_job_removal(job_key, "completed")
                
                # Publish completion event
                await self._publish_event("job:completed", {
                    "job_id": job_id,
                    "job_name": job.name,
                    "result": result,
                    "duration": duration
                })
                
                print(f"✅ Job {job_id} completed in {duration}ms")
                
            except UnrecoverableError as error:
                # Job failed with unrecoverable error - don't retry
                await self._handle_job_failure(job, str(error), False)
                
            except Exception as error:
                # Job failed - check if we should retry
                should_retry = job.attempts_made + 1 < job.options.attempts
                await self._handle_job_failure(job, str(error), should_retry)
                
        except Exception as error:
            print(f"❌ Error processing job {job_id}: {error}")
    
    async def _handle_job_failure(self, job: JobData, error_message: str, should_retry: bool) -> None:
        """Handle job failure with retry logic."""
        # Implementation continues in next part...
        pass
    
    async def _handle_job_removal(self, job_key: str, status: str) -> None:
        """Handle job removal based on configuration."""
        # Implementation continues in next part...
        pass
    
    def _calculate_backoff(self, attempt: int, backoff_options: BackoffOptions, error_message: str = None) -> int:
        """Calculate backoff delay for retry attempts."""
        # Implementation continues in next part...
        return 1000
    
    async def _publish_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publish an event to the events stream."""
        # Implementation continues in next part...
        pass
    
    async def _heartbeat_loop(self) -> None:
        """Maintain worker heartbeat in Redis."""
        # Implementation continues in next part...
        pass
    
    async def _stalled_check_loop(self) -> None:
        """Check for and recover stalled jobs."""
        # Implementation continues in next part...
        pass
    
    async def _delayed_jobs_loop(self) -> None:
        """Process delayed jobs that are ready to execute."""
        # Implementation continues in next part...
        pass
    
    async def _recover_stalled_jobs(self) -> None:
        """Recover jobs that have stalled (lost their locks)."""
        # Implementation continues in next part...
        pass
    
    async def _recover_stalled_job(self, job_id: str, lock_data: Dict[str, Any]) -> None:
        """Recover a single stalled job."""
        # Implementation continues in next part...
        pass 