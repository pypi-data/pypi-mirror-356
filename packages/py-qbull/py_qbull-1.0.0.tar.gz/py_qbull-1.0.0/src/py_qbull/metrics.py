"""
Metrics class for collecting and analyzing queue performance data.

This module provides real-time monitoring, historical data storage,
and performance statistics for PyBull job queues.
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
import redis
import redis.asyncio as aioredis

from .types import (
    MetricsOptions, JobCounts, MetricsDataPoint, MetricsMetadata,
    HistoricalMetrics, PerformanceStats, MetricsEvent
)
from .errors import MetricsError


class Metrics:
    """
    Metrics class for collecting and analyzing queue performance data.
    
    Provides real-time monitoring, historical data storage, and performance statistics.
    Designed to work efficiently in distributed environments like Kubernetes.
    """
    
    def __init__(self, app_name: str, queue_name: str, options: MetricsOptions):
        """
        Initialize a new Metrics instance.
        
        Args:
            app_name: Application name for namespacing
            queue_name: Queue name for identification
            options: Metrics configuration options
        """
        self.app_name = app_name
        self.queue_name = queue_name
        self.prefix = f"{app_name}:{queue_name}"
        self.connection = options.connection
        
        # Configuration
        self.interval = options.interval / 1000.0  # Convert to seconds
        self.retention = options.retention
        
        # Background task
        self._metrics_task: Optional[asyncio.Task] = None
        self._is_collecting = False
        
        # Event callbacks
        self._event_callbacks: List[callable] = []
    
    async def start_metrics_collection(self) -> None:
        """
        Start the metrics collection process.
        
        Begins periodic collection of queue metrics and emits events.
        """
        if self._is_collecting:
            return
        
        self._is_collecting = True
        self._metrics_task = asyncio.create_task(self._collection_loop())
        print(f"📊 Metrics collection started for {self.prefix}")
    
    def stop_metrics_collection(self) -> None:
        """
        Stop the metrics collection process.
        
        Cancels the collection task and cleans up resources.
        """
        if not self._is_collecting:
            return
        
        self._is_collecting = False
        
        if self._metrics_task and not self._metrics_task.done():
            self._metrics_task.cancel()
        
        print(f"📊 Metrics collection stopped for {self.prefix}")
    
    def on_metrics(self, callback: callable) -> None:
        """
        Register a callback for metrics events.
        
        Args:
            callback: Function to call when metrics are collected
        """
        self._event_callbacks.append(callback)
    
    async def _collection_loop(self) -> None:
        """Main metrics collection loop."""
        while self._is_collecting:
            try:
                await self._collect_metrics()
                await asyncio.sleep(self.interval)
                
            except Exception as error:
                print(f"⚠️ Error in metrics collection: {error}")
                await asyncio.sleep(self.interval)
    
    async def _collect_metrics(self) -> None:
        """
        Collect metrics from the queue at a specific point in time.
        
        Stores the data in Redis and emits a metrics event.
        """
        timestamp = int(time.time() * 1000)
        counts = await self.get_job_counts()
        
        # Store metrics in Redis
        await self._store_metrics(timestamp, counts)
        
        # Create metrics event
        event = MetricsEvent(
            timestamp=timestamp,
            counts=counts,
            performance=await self._calculate_performance_stats(timestamp)
        )
        
        # Emit event to callbacks
        for callback in self._event_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as error:
                print(f"⚠️ Error in metrics callback: {error}")
    
    async def _store_metrics(self, timestamp: int, counts: JobCounts) -> None:
        """
        Store metrics data in Redis.
        
        Uses hash for metadata and list for time series data.
        
        Args:
            timestamp: When the metrics were collected
            counts: Job counts by state
        """
        try:
            if isinstance(self.connection, aioredis.Redis):
                pipe = self.connection.pipeline()
            else:
                pipe = self.connection.pipeline()
            
            # Store counters by type
            for count_type, count in [
                ("waiting", counts.waiting),
                ("processing", counts.processing), 
                ("completed", counts.completed),
                ("failed", counts.failed)
            ]:
                metrics_key = f"{self.prefix}:metrics:{count_type}"
                data_key = f"{metrics_key}:data"
                
                # Store metadata
                pipe.hset(metrics_key, mapping={
                    "count": str(count),
                    "prev_timestamp": str(timestamp),
                    "prev_count": str(count)
                })
                
                # Store time series data
                data_point = json.dumps({"timestamp": timestamp, "count": count})
                pipe.lpush(data_key, data_point)
                pipe.ltrim(data_key, 0, self.retention - 1)
            
            if isinstance(self.connection, aioredis.Redis):
                await pipe.execute()
            else:
                pipe.execute()
                
        except Exception as error:
            raise MetricsError(f"Failed to store metrics: {error}", operation="store")
    
    async def get_job_counts(self) -> JobCounts:
        """
        Get current job counts by state.
        
        Scans Redis to count jobs in different states.
        
        Returns:
            JobCounts with current state counts
        """
        try:
            counts = JobCounts()
            
            # Count waiting jobs (lists by group)
            groups_set_key = f"{self.prefix}:groups:set"
            
            if isinstance(self.connection, aioredis.Redis):
                groups = await self.connection.smembers(groups_set_key)
                groups = [g.decode() if isinstance(g, bytes) else g for g in groups]
                
                # Count waiting jobs in groups
                pipe = self.connection.pipeline()
                for group in groups:
                    pipe.llen(f"{self.prefix}:groups:{group}")
                    pipe.zcard(f"{self.prefix}:priority:{group}")
                
                if groups:
                    results = await pipe.execute()
                    for i in range(0, len(results), 2):
                        counts.waiting += results[i] + results[i + 1]
            
            else:
                # Synchronous version
                groups = self.connection.smembers(groups_set_key)
                groups = [g.decode() if isinstance(g, bytes) else g for g in groups]
                
                # Count waiting jobs in groups
                for group in groups:
                    counts.waiting += self.connection.llen(f"{self.prefix}:groups:{group}")
                    counts.waiting += self.connection.zcard(f"{self.prefix}:priority:{group}")
            
            return counts
            
        except Exception as error:
            raise MetricsError(f"Failed to get job counts: {error}", operation="count")
    
    async def get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics with real-time job counts and basic historical data.
        
        Returns:
            Dictionary with current metrics and metadata
        """
        try:
            current_counts = await self.get_job_counts()
            timestamp = int(time.time() * 1000)
            
            # Check if we have historical data
            has_historical = False
            recent_activity = {"completed": 0, "failed": 0, "success_rate": 0.0}
            
            try:
                # Get recent completed/failed counts for activity calculation
                completed_data = await self._get_recent_data("completed", 10)
                failed_data = await self._get_recent_data("failed", 10)
                
                if completed_data or failed_data:
                    has_historical = True
                    recent_completed = sum(point["count"] for point in completed_data)
                    recent_failed = sum(point["count"] for point in failed_data)
                    total_recent = recent_completed + recent_failed
                    
                    recent_activity = {
                        "completed": recent_completed,
                        "failed": recent_failed,
                        "success_rate": (recent_completed / total_recent * 100) if total_recent > 0 else 0.0
                    }
                    
            except Exception:
                pass  # Use defaults if historical data unavailable
            
            return {
                "current": current_counts,
                "timestamp": timestamp,
                "has_historical_data": has_historical,
                "recent_activity": recent_activity
            }
            
        except Exception as error:
            raise MetricsError(f"Failed to get current metrics: {error}", operation="current")
    
    async def get_basic_metrics(self) -> Dict[str, Any]:
        """
        Get basic metrics summary.
        
        Returns:
            Dictionary with basic metrics and totals
        """
        try:
            counts = await self.get_job_counts()
            timestamp = int(time.time() * 1000)
            
            total = counts.waiting + counts.processing + counts.completed + counts.failed
            
            return {
                "waiting": counts.waiting,
                "processing": counts.processing,
                "completed": counts.completed,
                "failed": counts.failed,
                "total": total,
                "timestamp": timestamp
            }
            
        except Exception as error:
            raise MetricsError(f"Failed to get basic metrics: {error}", operation="basic")
    
    async def get_metrics(
        self, 
        metric_type: str, 
        start: int = 0, 
        end: int = -1
    ) -> HistoricalMetrics:
        """
        Get historical metrics for a specific type.
        
        Args:
            metric_type: Type of metric ("waiting", "processing", "completed", "failed")
            start: Start index for data range
            end: End index for data range (-1 for all)
            
        Returns:
            HistoricalMetrics with metadata and data points
        """
        try:
            if metric_type not in ["waiting", "processing", "completed", "failed"]:
                raise MetricsError(f"Invalid metric type: {metric_type}")
            
            data_key = f"{self.prefix}:metrics:{metric_type}:data"
            
            if isinstance(self.connection, aioredis.Redis):
                raw_data = await self.connection.lrange(data_key, start, end)
            else:
                raw_data = self.connection.lrange(data_key, start, end)
            
            # Parse data points
            data_points = []
            for raw_point in raw_data:
                if isinstance(raw_point, bytes):
                    raw_point = raw_point.decode()
                
                try:
                    point_data = json.loads(raw_point)
                    data_points.append(MetricsDataPoint(
                        timestamp=point_data["timestamp"],
                        counts=JobCounts(**{metric_type: point_data["count"]})
                    ))
                except (json.JSONDecodeError, KeyError):
                    continue  # Skip invalid data points
            
            # Create metadata
            metadata = MetricsMetadata(
                queue_name=self.queue_name,
                app_name=self.app_name,
                collection_interval=int(self.interval * 1000),
                retention_period=self.retention
            )
            
            return HistoricalMetrics(
                metadata=metadata,
                data_points=data_points,
                total_points=len(data_points)
            )
            
        except Exception as error:
            raise MetricsError(f"Failed to get metrics for {metric_type}: {error}", operation="historical")
    
    async def get_performance_stats(self, time_window: int = 3600000) -> PerformanceStats:
        """
        Get performance statistics for a time window.
        
        Args:
            time_window: Time window in milliseconds (default: 1 hour)
            
        Returns:
            PerformanceStats with calculated statistics
        """
        try:
            current_time = int(time.time() * 1000)
            start_time = current_time - time_window
            
            # Get completed and failed job data
            completed_data = await self._get_recent_data("completed", -1)
            failed_data = await self._get_recent_data("failed", -1)
            
            # Filter data within time window
            completed_in_window = [
                point for point in completed_data 
                if point["timestamp"] >= start_time
            ]
            failed_in_window = [
                point for point in failed_data 
                if point["timestamp"] >= start_time
            ]
            
            jobs_completed = sum(point["count"] for point in completed_in_window)
            jobs_failed = sum(point["count"] for point in failed_in_window)
            jobs_processed = jobs_completed + jobs_failed
            
            # Calculate statistics
            success_rate = (jobs_completed / jobs_processed * 100) if jobs_processed > 0 else 0.0
            error_rate = (jobs_failed / jobs_processed * 100) if jobs_processed > 0 else 0.0
            throughput = jobs_processed / (time_window / 1000.0)  # jobs per second
            
            # Calculate average processing time (simplified - would need job timing data)
            average_processing_time = 0.0  # Would require additional timing metrics
            
            return PerformanceStats(
                time_window=time_window,
                jobs_processed=jobs_processed,
                jobs_failed=jobs_failed,
                average_processing_time=average_processing_time,
                throughput=throughput,
                success_rate=success_rate,
                error_rate=error_rate
            )
            
        except Exception as error:
            raise MetricsError(f"Failed to get performance stats: {error}", operation="performance")
    
    async def _get_recent_data(self, metric_type: str, count: int) -> List[Dict[str, Any]]:
        """
        Get recent data points for a metric type.
        
        Args:
            metric_type: Type of metric
            count: Number of recent points to get (-1 for all)
            
        Returns:
            List of data point dictionaries
        """
        data_key = f"{self.prefix}:metrics:{metric_type}:data"
        
        try:
            if isinstance(self.connection, aioredis.Redis):
                raw_data = await self.connection.lrange(data_key, 0, count - 1 if count > 0 else -1)
            else:
                raw_data = self.connection.lrange(data_key, 0, count - 1 if count > 0 else -1)
            
            data_points = []
            for raw_point in raw_data:
                if isinstance(raw_point, bytes):
                    raw_point = raw_point.decode()
                
                try:
                    point_data = json.loads(raw_point)
                    data_points.append(point_data)
                except (json.JSONDecodeError, KeyError):
                    continue
            
            return data_points
            
        except Exception:
            return []
    
    async def _calculate_performance_stats(self, timestamp: int) -> Optional[PerformanceStats]:
        """
        Calculate performance stats for the current collection cycle.
        
        Args:
            timestamp: Current timestamp
            
        Returns:
            PerformanceStats or None if insufficient data
        """
        try:
            # Use a 5-minute window for performance calculation
            time_window = 5 * 60 * 1000  # 5 minutes in milliseconds
            return await self.get_performance_stats(time_window)
            
        except Exception:
            return None  # Return None if performance stats can't be calculated
    
    async def clean_old_metrics(self, max_age: int = 7 * 24 * 60 * 60 * 1000) -> None:
        """
        Clean old metrics data beyond the retention period.
        
        Args:
            max_age: Maximum age in milliseconds (default: 7 days)
        """
        try:
            current_time = int(time.time() * 1000)
            cutoff_time = current_time - max_age
            
            metric_types = ["waiting", "processing", "completed", "failed"]
            
            for metric_type in metric_types:
                data_key = f"{self.prefix}:metrics:{metric_type}:data"
                
                # Get all data and filter out old entries
                if isinstance(self.connection, aioredis.Redis):
                    all_data = await self.connection.lrange(data_key, 0, -1)
                else:
                    all_data = self.connection.lrange(data_key, 0, -1)
                
                # Filter recent data
                recent_data = []
                for raw_point in all_data:
                    if isinstance(raw_point, bytes):
                        raw_point = raw_point.decode()
                    
                    try:
                        point_data = json.loads(raw_point)
                        if point_data["timestamp"] >= cutoff_time:
                            recent_data.append(raw_point)
                    except (json.JSONDecodeError, KeyError):
                        continue
                
                # Replace data with filtered version
                if isinstance(self.connection, aioredis.Redis):
                    pipe = self.connection.pipeline()
                    pipe.delete(data_key)
                    if recent_data:
                        pipe.lpush(data_key, *recent_data)
                    await pipe.execute()
                else:
                    pipe = self.connection.pipeline()
                    pipe.delete(data_key)
                    if recent_data:
                        pipe.lpush(data_key, *recent_data)
                    pipe.execute()
            
            print(f"🧹 Cleaned old metrics data (older than {max_age}ms)")
            
        except Exception as error:
            print(f"⚠️ Error cleaning old metrics: {error}") 