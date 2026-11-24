import pytest

from swarmforge.backoff_policies_and_metrics import (
    BackoffPolicy,
    SwarmLevelMetrics,
    BackoffPoliciesAndMetricsConfig,
)

def test_backoff_policy_validation():
    with pytest.raises(ValueError):
        BackoffPolicy(type="fixed", initial_delay=5, maximum_delay=3)

def test_backoff_policy_initial_delay_no_multiplier():
    bp = BackoffPolicy(type="fixed", initial_delay=1)
    assert bp.multiplier == 2

def test_backoff_policy_no_maximum_delay():
    bp = BackoffPolicy(type="fixed", initial_delay=1, multiplier=2)
    assert bp.maximum_delay is None

def test_swarm_level_metrics_validation():
    with pytest.raises(ValueError):
        SwarmLevelMetrics(success_rate=0.5, failure_rate=0.6)

def test_swarm_level_metrics_response_time_optional():
    slm = SwarmLevelMetrics(success_rate=0.5, failure_rate=0.5)
    assert slm.response_time is None

def test_backoff_policies_and_metrics_config_validation():
    with pytest.raises(ValueError):
        BackoffPoliciesAndMetricsConfig(
            backoff_policies={"fixed": BackoffPolicy(type="fixed", initial_delay=5, maximum_delay=3)},
            swarm_level_metrics=SwarmLevelMetrics(success_rate=0.5, failure_rate=0.6),
        )
