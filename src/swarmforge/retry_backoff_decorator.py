import time
from typing import Callable
from swarmforge.backoff_policies_and_metrics import ExponentialBackoff

def retry_on_role_assignment_failure(max_retries: int = 5, backoff_policy: ExponentialBackoff = None) -> Callable:
    """Retry decorator for role assignment functions.

    Args:
        max_retries (int, optional): Maximum number of retries. Defaults to 5.
        backoff_policy (ExponentialBackoff, optional): Custom backoff policy. Defaults to None.

    Returns:
        Callable: Decorator function.
    """
    if backoff_policy is None:
        backoff_policy = ExponentialBackoff(initial=1, factor=2, max_value=60)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except RoleAssignmentError as e:
                    message = f"Role assignment failed. Retrying. Error: {e}"
                    print(message)
                    retries += 1
                    wait_time = backoff_policy.backoff(retries)
                    time.sleep(wait_time)
            raise RoleAssignmentError("Max retries exceeded") from None
        return wrapper
    return decorator
