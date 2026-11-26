import pytest
from swarmforge.backoff_policies_and_metrics import BackoffPolicy, SwarmLevelMetrics

def test_backoff_policy_initial_delay():
    bp = BackoffPolicy(type='test', initial_delay=5)
    assert bp.initial_delay == 5

def test_backoff_policy_multiplier():
    bp = BackoffPolicy(type='test', multiplier=3)
    assert bp.multiplier == 3

def test_backoff_policy_maximum_delay():
    bp = BackoffPolicy(type='test', maximum_delay=10)
    assert bp.maximum_delay == 10

def test_backoff_policy_invalid_maximum_delay():
    with pytest.raises(ValueError):
        BackoffPolicy(type='test', initial_delay=10, maximum_delay=5)

def test_swarm_level_metrics_success_rate():
    metrics = SwarmLevelMetrics(success_rate=0.6, failure_rate=0.4)
    assert metrics.success_rate == 0.6

def test_swarm_level_metrics_failure_rate():
    metrics = SwarmLevelMetrics(success_rate=0.6, failure_rate=0.4)
    assert metrics.failure_rate == 0.4

def test_swarm_level_metrics_invalid_success_failure_rate():
    with pytest.raises(ValueError):
        SwarmLevelMetrics(success_rate=0.6, failure_rate=1.0)

def test_swarm_level_metrics_average_throughput():
    metrics = SwarmLevelMetrics(success_rate=0.6, failure_rate=0.4, average_throughput=10.0)
    assert metrics.average_throughput == 10.0

def test_swarm_level_metrics_response_time():
    metrics = SwarmLevelMetrics(success_rate=0.6, failure_rate=0.4, response_time=5.0)
    assert metrics.response_time == 5.0
