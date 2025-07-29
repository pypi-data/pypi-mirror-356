import time
import asyncio
import inspect
from typing import Callable, Optional, TypeVar, Any, Tuple, Dict

from meseex.mr_meseex import MrMeseex, TaskException
from meseex.control_flow.signals import TaskSignal, Repeat
from meseex.utils import _expects_mr_meseex_param

# Type variable for better type hinting
T = TypeVar('T')
POLLING_STATE_KEY = "_polling_state"


class PollAgain(TaskSignal):
    """
    Signal returned by a user's task function (wrapped by @polling_task)
    to indicate that polling should continue.
    
    Example:
        @polling_task(timeout_seconds=60)
        async def wait_for_job(meex: MrMeseex):
            status = await check_job_status(job_id)
            if status == "COMPLETED":
                return status
            return PollAgain(f"Job status: {status}")
    """
    pass


class PollingException(TaskException):
    """
    Exception raised when a polling task fails due to timeout or max retries.

    Provides detailed information about the polling failure and preserves the original error
    to help with debugging.
    """
    def __init__(
        self,
        message: str,
        task: Optional[str] = None,
        method_reference: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        # Store method reference which is polling-specific
        self.method_reference = method_reference

        # Create a clear, informative error message
        task_name = task or "unknown"
        if method_reference:
            full_message = f"Polling task '{task_name}' failed in {method_reference}: {message}"
        else:
            full_message = f"Polling task '{task_name}' failed: {message}"

        # Call parent constructor with the full message
        super().__init__(
            message=full_message,
            task=task,
            original_error=original_error
        )


class PollingState:
    """
    Internal state tracker for polling operations.
    
    Tracks timing, retries, and preserves error information between attempts.
    """
    def __init__(self, poll_interval_s: float = 1, timeout_s: float = 300.0):
        self.start_time: float = time.monotonic()
        self.poll_interval: float = poll_interval_s
        self.timeout: float = timeout_s
        self.last_exception: Optional[Exception] = None
        
    @property
    def elapsed_time(self) -> float:
        """Returns the time elapsed since polling started."""
        return time.monotonic() - self.start_time
    
    @property
    def remaining_time(self) -> float:
        """Returns the time remaining before timeout."""
        return max(0.0, self.timeout - self.elapsed_time)

    @property
    def is_timeout(self) -> bool:
        """Checks if polling has timed out."""
        return self.elapsed_time > self.timeout


def _get_or_create_polling_state(meex: MrMeseex, poll_interval_s: float, timeout_s: float):
    """Gets existing polling state or initializes a new one."""

    state = meex.get_task_signal(POLLING_STATE_KEY)
    
    if state is None:
        # First execution: initialize state
        state = PollingState(poll_interval_s=poll_interval_s, timeout_s=timeout_s)
        meex.set_task_signal(POLLING_STATE_KEY, state)
        meex.set_task_progress(0.0, "Polling initiated")
        
    return state


def _handle_poll_again(meex: MrMeseex, result: T, state: PollingState, func: Callable) -> T:
    if not isinstance(result, PollAgain):
        meex.clear_task_data(POLLING_STATE_KEY)
        meex.set_task_progress(None, "Polling completed")
        return result
                
    # Handle PollAgain logic
    if state.is_timeout:
        raise PollingException(
            message="Polling timed out",
            task=meex.task,
            method_reference=f"{func.__module__}.{func.__qualname__}",
            original_error=getattr(state, 'last_exception', None)
        )

    return Repeat(delay_s=state.poll_interval)


def _is_class_method(func: Callable) -> bool:
    """Check if function is a class method by examining first parameter."""
    sig = inspect.signature(func)
    return bool(sig.parameters) and next(iter(sig.parameters.values())).name in ('self', 'cls')

        
def polling_task(poll_interval_seconds: float = 1.0, timeout_seconds: float = 300.0) -> Callable[[Callable], Callable]:
    """
    Transforms a function into a polling task that automatically retries until success or timeout.
    
    The decorated function should perform a single polling attempt and either:
    - Return a value on success
    - Return PollAgain to continue polling
    
    Works with both async and sync functions, and supports both regular functions and class methods.
    
    Example:
        @polling_task(poll_interval_seconds=5, timeout_seconds=60)
        async def check_job_status(meex: MrMeseex) -> str:
            status = await check_status(meex.data["job_id"])
            if status in ("COMPLETED", "FAILED"):
                return status  # Success, return final status
            return PollAgain(f"Job status: {status}")  # Continue polling

        # Also works with class methods:
        class MyService:
            @polling_task(poll_interval_seconds=2)
            async def poll_endpoint(self, meex: MrMeseex):
                # self is properly handled, meex is correctly passed
                return PollAgain() if not_ready() else result
    
    Args:
        poll_interval_seconds: Time to wait between polling attempts
        timeout_seconds: Maximum total time to spend polling before failing
    
    Returns:
        Decorator function that wraps the target function
    """
    def decorator(func: Callable) -> Callable:
        is_async = asyncio.iscoroutinefunction(func)
        is_class_method = _is_class_method(func)
        expects_meex = _expects_mr_meseex_param(func)
            
        async def async_poll_class_method_wrapper(self, meex: MrMeseex):
            state = _get_or_create_polling_state(meex, poll_interval_seconds, timeout_seconds)
            if not expects_meex:
                result = await func(self)
            else:
                result = await func(self, meex)
                
            return _handle_poll_again(meex, result, state, func)

        # Async wrapper for async functions
        async def async_poll_wrapper(meex: MrMeseex):
            state = _get_or_create_polling_state(meex, poll_interval_seconds, timeout_seconds)  
            if expects_meex:
                result = await func(meex)
            else:
                result = await func()

            # Handle the result for polling continuation
            return _handle_poll_again(meex, result, state, func)
            
        def sync_poll_class_method_wrapper(self, meex: MrMeseex):
            state = _get_or_create_polling_state(meex, poll_interval_seconds, timeout_seconds)
            if not expects_meex:
                result = func(self)
            else:
                result = func(self, meex)
            return _handle_poll_again(meex, result, state, func)

        def sync_poll_wrapper(meex: MrMeseex):
            state = _get_or_create_polling_state(meex, poll_interval_seconds, timeout_seconds)
            if expects_meex:
                result = func(meex)
            else:
                result = func()
            return _handle_poll_again(meex, result, state, func)
        
        # Return the appropriate wrapper based on the function type
        if is_class_method:
            return async_poll_class_method_wrapper if is_async else sync_poll_class_method_wrapper
        else:
            return async_poll_wrapper if is_async else sync_poll_wrapper
            
    return decorator
