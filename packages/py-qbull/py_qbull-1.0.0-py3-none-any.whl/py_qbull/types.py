"""
Type definitions for PyBull job queue library.

This module contains all the type definitions, data classes, and protocols
used throughout the PyBull library for type safety and better IDE support.
"""

from typing import Dict, List, Optional, Union, Callable, Any, Protocol, Literal
from dataclasses import dataclass, field
from enum import Enum
import redis
from datetime import datetime


# Redis connection type
RedisConnection = Union[redis.Redis, redis.asyncio.Redis]


class BackoffStrategy(str, Enum):
    """Backoff strategy types for job retries."""
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"


@dataclass
class RateLimitOptions:
    """Rate limiting configuration options."""
    max: int = 0  # Maximum number of jobs, 0 = no limit
    duration: int = 0  # Time window in milliseconds, 0 = no limit


@dataclass
class BackoffOptions:
    """Backoff configuration for job retries."""
    type: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    delay: int = 1000  # Initial delay in milliseconds
    max_delay: int = 300000  # Maximum delay in milliseconds (5 minutes)
    jitter: Union[bool, int] = False  # Add randomness to delay
    strategy: Optional[Callable[[int, Any, Optional[Exception]], int]] = None


@dataclass
class JobOptions:
    """Configuration options for individual jobs."""
    attempts: int = 3
    backoff: Optional[BackoffOptions] = None
    remove_on_complete: Union[bool, int] = False
    remove_on_fail: Union[bool, int] = False
    priority: int = 0
    delay: int = 0  # Delay before processing in milliseconds
    job_id: Optional[str] = None
    
    def __post_init__(self):
        if self.backoff is None:
            self.backoff = BackoffOptions()


@dataclass
class QueueOptions:
    """Configuration options for Queue instances."""
    connection: RedisConnection
    rate_limit: Optional[RateLimitOptions] = None
    
    def __post_init__(self):
        if self.rate_limit is None:
            self.rate_limit = RateLimitOptions()


@dataclass
class WorkerOptions:
    """Configuration options for Worker instances."""
    connection: RedisConnection
    concurrency: int = 1
    group_concurrency: Optional[int] = None
    groups: Optional[List[str]] = None
    remove_on_complete: Union[bool, int] = False
    remove_on_fail: Union[bool, int] = 5000
    batch_size: Optional[int] = None
    poll_interval: int = 100  # milliseconds
    stall_interval: int = 5000  # milliseconds
    lock_duration: int = 30000  # milliseconds
    max_stalled_count: int = 3
    backoff: Optional[BackoffOptions] = None
    heartbeat_interval: int = 5000  # milliseconds
    stalled_check_interval: int = 30000  # milliseconds
    stalled_timeout: Optional[int] = None
    
    def __post_init__(self):
        if self.group_concurrency is None:
            self.group_concurrency = max(1, self.concurrency // 4)
        if self.batch_size is None:
            self.batch_size = min(10, max(1, self.concurrency // 10))
        if self.stalled_timeout is None:
            self.stalled_timeout = self.lock_duration * 2
        if self.backoff is None:
            self.backoff = BackoffOptions()


@dataclass
class MetricsOptions:
    """Configuration options for Metrics instances."""
    connection: RedisConnection
    interval: int = 60000  # Collection interval in milliseconds
    retention: int = 1440  # Data retention in minutes (24 hours)


# Job data and processor types
@dataclass
class JobData:
    """Data structure for job information."""
    id: str
    name: str
    data: Dict[str, Any]
    options: JobOptions
    timestamp: int
    attempts_made: int = 0
    processed_on: Optional[int] = None
    finished_on: Optional[int] = None
    failed_reason: Optional[str] = None
    group: str = "default"
    status: Literal["waiting", "processing", "completed", "failed", "delayed"] = "waiting"


class JobProcessor(Protocol):
    """Protocol for job processing functions."""
    
    async def __call__(self, job: JobData) -> Any:
        """Process a job and return the result."""
        ...


# Event data structures
@dataclass
class JobCompletedEvent:
    """Event emitted when a job completes successfully."""
    job_id: str
    result: Any
    duration: int  # Processing time in milliseconds


@dataclass
class JobFailedEvent:
    """Event emitted when a job fails."""
    job_id: str
    error: str
    attempts_made: int
    will_retry: bool


@dataclass
class JobStalledEvent:
    """Event emitted when a job is detected as stalled."""
    job_id: str
    stalled_count: int


@dataclass
class JobRetriesExhaustedEvent:
    """Event emitted when a job has exhausted all retry attempts."""
    job_id: str
    final_error: str
    total_attempts: int


# Callback types
@dataclass
class JobCallbacks:
    """Callback functions for job events."""
    on_completed: Optional[Callable[[JobCompletedEvent], None]] = None
    on_failed: Optional[Callable[[JobFailedEvent], None]] = None
    on_stalled: Optional[Callable[[JobStalledEvent], None]] = None
    on_retries_exhausted: Optional[Callable[[JobRetriesExhaustedEvent], None]] = None


# Status and info structures
@dataclass
class WorkerInfo:
    """Information about a worker instance."""
    worker_id: str
    hostname: str
    pid: int
    started_at: datetime
    last_heartbeat: datetime
    processing_jobs: List[str]


@dataclass
class QueueStatus:
    """Current status of a queue."""
    waiting: int
    processing: int
    completed: int
    failed: int
    delayed: int
    total_workers: int
    active_workers: int
    workers: List[WorkerInfo]


# Metrics types
@dataclass
class JobCounts:
    """Job counts by status."""
    waiting: int = 0
    processing: int = 0
    completed: int = 0
    failed: int = 0


@dataclass
class MetricsDataPoint:
    """Single metrics data point."""
    timestamp: int
    counts: JobCounts


@dataclass
class MetricsMetadata:
    """Metadata for metrics collection."""
    queue_name: str
    app_name: str
    collection_interval: int
    retention_period: int


@dataclass
class HistoricalMetrics:
    """Historical metrics data."""
    metadata: MetricsMetadata
    data_points: List[MetricsDataPoint]
    total_points: int


@dataclass
class PerformanceStats:
    """Performance statistics for a time window."""
    time_window: int  # milliseconds
    jobs_processed: int
    jobs_failed: int
    average_processing_time: float
    throughput: float  # jobs per second
    success_rate: float  # percentage
    error_rate: float  # percentage


@dataclass
class MetricsEvent:
    """Event emitted during metrics collection."""
    timestamp: int
    counts: JobCounts
    performance: Optional[PerformanceStats] = None 