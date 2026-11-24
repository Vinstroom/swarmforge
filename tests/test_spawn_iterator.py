from src.swarmforge.spawn_iterator import spawn_iterator
from src.swarmforge.timestamp import get_timestamp
import time
import pytest

def test_no_prev_timestamp():
    iterator = spawn_iterator(0.5, 0.1)
    assert next(iterator) == (0, 0)

def test_interval_within_range():
    iterator = spawn_iterator(0.5, 0.1)
    prev_diff = next(iterator)[1]
    for _ in range(10):
        diff = next(iterator)[1]
        assert 0.09 < diff < 0.11

def test_interval_too_large():
    iterator = spawn_iterator(0.2, 0.1)
    time.sleep(0.3)  # Delay to make the next timestamp's interval too large
    with pytest.raises(ValueError):
        next(iterator)

def test_timeout_exceeded():
    iterator = spawn_iterator(0.5, 0.1)
    time.sleep(1.0)  # Delay to exceed the timeout
    with pytest.raises(TimeoutError):
        next(iterator)
