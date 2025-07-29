"""
Custom exception classes for PyBull job queue library.

This module defines all custom exceptions that can be raised by PyBull
components during job processing and queue operations.
"""


class PyBullError(Exception):
    """
    Base exception class for all PyBull-related errors.
    
    All custom exceptions in PyBull inherit from this base class,
    making it easy to catch any PyBull-specific error.
    """
    pass


class RateLimitError(PyBullError):
    """
    Raised when a rate limit is exceeded.
    
    This exception is thrown when trying to add jobs to a queue
    that has reached its configured rate limit, either globally
    or for a specific group.
    
    Attributes:
        message: Human-readable error message
        retry_after: Time in milliseconds until rate limit resets
        limit_type: Type of rate limit ('global' or 'group')
        group_id: Group ID if this is a group-specific rate limit
    """
    
    def __init__(
        self, 
        message: str, 
        retry_after: int = 0,
        limit_type: str = "global",
        group_id: str = None
    ):
        super().__init__(message)
        self.retry_after = retry_after
        self.limit_type = limit_type
        self.group_id = group_id


class UnrecoverableError(PyBullError):
    """
    Raised when a job encounters an unrecoverable error.
    
    Jobs that raise this exception will not be retried,
    regardless of the retry configuration. This is useful
    for errors that are guaranteed to fail on retry, such as
    invalid input data or missing required resources.
    
    Attributes:
        message: Human-readable error message
        job_id: ID of the job that failed
        original_error: The original exception that caused this error
    """
    
    def __init__(
        self, 
        message: str, 
        job_id: str = None,
        original_error: Exception = None
    ):
        super().__init__(message)
        self.job_id = job_id
        self.original_error = original_error


class JobNotFoundError(PyBullError):
    """
    Raised when trying to access a job that doesn't exist.
    
    This exception is thrown when attempting to retrieve,
    retry, or modify a job that cannot be found in the queue.
    
    Attributes:
        job_id: ID of the job that was not found
    """
    
    def __init__(self, job_id: str):
        super().__init__(f"Job with ID '{job_id}' not found")
        self.job_id = job_id


class WorkerError(PyBullError):
    """
    Raised when a worker encounters an error during operation.
    
    This exception covers various worker-related errors such as
    connection issues, configuration problems, or processing failures.
    
    Attributes:
        message: Human-readable error message
        worker_id: ID of the worker that encountered the error
        operation: The operation that was being performed when the error occurred
    """
    
    def __init__(
        self, 
        message: str, 
        worker_id: str = None,
        operation: str = None
    ):
        super().__init__(message)
        self.worker_id = worker_id
        self.operation = operation


class QueueError(PyBullError):
    """
    Raised when a queue encounters an error during operation.
    
    This exception covers various queue-related errors such as
    connection issues, configuration problems, or job management failures.
    
    Attributes:
        message: Human-readable error message
        queue_name: Name of the queue that encountered the error
        app_name: Application name associated with the queue
    """
    
    def __init__(
        self, 
        message: str, 
        queue_name: str = None,
        app_name: str = None
    ):
        super().__init__(message)
        self.queue_name = queue_name
        self.app_name = app_name


class MetricsError(PyBullError):
    """
    Raised when metrics collection or processing fails.
    
    This exception is thrown when there are issues with
    collecting, storing, or retrieving metrics data.
    
    Attributes:
        message: Human-readable error message
        operation: The metrics operation that failed
    """
    
    def __init__(self, message: str, operation: str = None):
        super().__init__(message)
        self.operation = operation


class ConnectionError(PyBullError):
    """
    Raised when there are Redis connection issues.
    
    This exception is thrown when PyBull cannot connect to
    Redis or loses connection during operation.
    
    Attributes:
        message: Human-readable error message
        redis_error: The original Redis exception
    """
    
    def __init__(self, message: str, redis_error: Exception = None):
        super().__init__(message)
        self.redis_error = redis_error


class ConfigurationError(PyBullError):
    """
    Raised when there are configuration issues.
    
    This exception is thrown when PyBull components are
    configured incorrectly or with invalid parameters.
    
    Attributes:
        message: Human-readable error message
        parameter: The configuration parameter that is invalid
        value: The invalid value that was provided
    """
    
    def __init__(
        self, 
        message: str, 
        parameter: str = None,
        value = None
    ):
        super().__init__(message)
        self.parameter = parameter
        self.value = value 