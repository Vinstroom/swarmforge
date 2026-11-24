import pytest

from swarmforge.task_queue_normalization import normalize_string, normalize_task_name

def test_normalize_string():
    assert normalize_string("Hello, World!") == "hello world"
    assert normalize_string("Python3.11") == "python3 11"
    assert normalize_string(" SwarmForge ") == "swarmforge"

def test_normalize_task_name():
    assert normalize_task_name("__init__") == "init"
    assert normalize_task_name("task_name") == "task_name"
    assert normalize_task_name("__main__") == "main"
