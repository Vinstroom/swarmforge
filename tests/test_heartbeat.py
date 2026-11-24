import pytest
from datetime import datetime, timedelta
from src.swarmforge.heartbeat import Heartbeats

def test_add_and_latest():
    hb = Heartbeats(capacity=2)
    agent_id = "agent1"

    # Add initial heartbeat
    hb.add(agent_id, datetime.now())
    assert hb.latest(agent_id) is not None

    # Add heartbeat after some time
    sleep_time = timedelta(seconds=1)
    sleep(sleep_time.total_seconds())
    hb.add(agent_id, datetime.now())
    assert hb.latest(agent_id) > hb.latest(agent_id) - sleep_time

    # Check that old heartbeat is removed due to capacity
    sleep_time = timedelta(seconds=2)
    sleep(sleep_time.total_seconds())
    assert hb.latest(agent_id) is None

def test_max_retries():
    hb = Heartbeats(max_retries=2)
    agent_id = "agent1"

    # Simulate missed heartbeats
    hb._heartbeats = []
    hb._retry_count[agent_id] = 3
    assert not hb._should_retry(agent_id)

    hb._retry_count[agent_id] = 1
    assert hb._should_retry(agent_id)

def test_reset():
    hb = Heartbeats()
    agent_id = "agent1"

    # Add heartbeat and then reset
    hb.add(agent_id, datetime.now())
    hb.reset()
    assert hb.latest(agent_id) is None

def test_as_millis():
    hb = Heartbeats()
    agent_id = "agent1"

    # Add heartbeat and check as_millis
    hb.add(agent_id, datetime.now())
    assert hb.as_millis()[agent_id] is not None
