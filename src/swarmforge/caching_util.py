import time
from typing import Callable, Any

# Decorator to cache the results of a function with a given TTL
def cache_results(ttl: int):
    """A decorator to cache the results of a function with a given time-to-live (TTL)."""

    def decorator(func: Callable) -> Callable:
        cache = {}

        def wrapper(*args, **kwargs) -> Any:
            key = (args, frozenset(kwargs.items()))
            if key in cache and time.time() - cache[key][1] < ttl:
                return cache[key][0]
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        return wrapper

    return decorator
