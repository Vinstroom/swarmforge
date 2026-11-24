from typing import Callable, Any, Optional
from functools import wraps
from time import time

Cache = dict[str, Optional[Any]]

def role_cache(max_age: int = 60) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to cache role assignment results.

    This decorator caches the result of a function for a given interval to reduce the
    overhead of repeated role assignment calculations.
    """
    cache: Cache = {}

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(kwargs.items()))
            if key in cache and time() - cache[key][0] < max_age:
                return cache[key][1]
            result = func(*args, **kwargs)
            cache[key] = (time(), result)
            return result
        return wrapper
    return decorator
