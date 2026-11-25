# tests/test_consensus_formatter_2.py

from typing import Any, List, Dict, Union, Callable, Optional
from swarmforge.consensus_formatter_2 import _format_value, format_consensus

def test_format_none():
    assert _format_value(None) == "- None"

def test_format_dict():
    fmt_dict = {"name": "John", "age": 30, "cars": ["Ford", "BMW"]}
    expected = '''name: John
age: 30
- cars
  - Ford
  - BMW'''
    assert _format_value(fmt_dict) == expected

def test_format_list():
    fmt_list = ["Ford", "BMW"]
    expected = '''- Ford
- BMW'''
    assert _format_value(fmt_list) == expected

def test_format_mixed():
    fmt_mixed = {"name": "John", "age": 30, "cars": {"model": "Ford", "year": 2020}}
    expected = '''name: John
age: 30
cars
  model: Ford
  year: 2020'''
    assert _format_value(fmt_mixed) == expected

def test_format_empty_consensus():
    assert format_consensus([]) == ""

def test_format_consensus():
    def mock_stats_func(consensus: List[Optional[TaskQueue]]) -> Dict[str, Any]:
        return {"total러스": 10, " erfolgreiche_rounts": 5}

    consensus = [
        {"arguments": {"name": "John", "age": 30}, "priority": 1},
        {"arguments": {"name": "Jane", "age": 25}, "priority": 2},
    ]
    expected = '''Task Queue 0:
name: John
age: 30
Priority: 1
Task Queue 1:
name: Jane
age: 25
Priority: 2
total_rounds: 10
erfolgreiche_rounts: 5'''
    assert format_consensus(consensus, mock_stats_func) == expected
