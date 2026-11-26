from functools import wraps
from typing import Callable
from time import time

class TaskQueueCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> any:
            key = (args, tuple(kwargs.items()))
            now = time()

            if key in self.cache and now - self.cache[key]['time'] < 60:  # Cache expires after 60 seconds
                return self.cache[key]['value']

            value = func(*args, **kwargs)
            self.cache[key] = {'value': value, 'time': now}

            if len(self.cache) > self.max_size:
                self.cache.pop(next(iter(self.cache)))

            return value

        return wrapper
