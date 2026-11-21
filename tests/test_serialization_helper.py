import json
import pytest
from swarmforge.serialization_helper import SwarmforgeSerializer
from swarmforge.backoff_policies_and_metrics import BackoffPoliciesAndMetrics
from swarmforge.consensus_metrics import ConsensusMetrics
from swarmforge.heartbeat_throughput import HeartbeatThroughput
from swarmforge.role_assignment_stats import RoleAssignmentStats
from swarmforge.swarm_state_machine import SwarmStateMachine

def test_serialize_backoff_policies_and_metrics():
    obj = BackoffPoliciesAndMetrics(backoff_policy="exponential", max_attempts=5)
    json_str = SwarmforgeSerializer.serialize(obj)
    deserialized_obj = json.loads(json_str)
    assert deserialized_obj == obj.model_dump()

def test_deserialize_backoff_policies_and_metrics():
    json_str = '{"backoff_policy": "exponential", "max_attempts": 5}'
    obj = SwarmforgeSerializer.deserialize(json_str, BackoffPoliciesAndMetrics)
    assert isinstance(obj, BackoffPoliciesAndMetrics)
    assert obj.backoff_policy == "exponential"
    assert obj.max_attempts == 5

def test_serialize_consensus_metrics():
    obj = ConsensusMetrics(consensus_cycle_duration=100, reached_consensus_count=5)
    json_str = SwarmforgeSerializer.serialize(obj)
    deserialized_obj = json.loads(json_str)
    assert deserialized_obj == obj.model_dump()

def test_deserialize_consensus_metrics():
    json_str = '{"consensus_cycle_duration": 100, "reached_consensus_count": 5}'
    obj = SwarmforgeSerializer.deserialize(json_str, ConsensusMetrics)
    assert isinstance(obj, ConsensusMetrics)
    assert obj.consensus_cycle_duration == 100
    assert obj.reached_consensus_count == 5

def test_serialize_heartbeat_throughput():
    obj = HeartbeatThroughput(total_heartbeats=100, total_messages=50)
    json_str = SwarmforgeSerializer.serialize(obj)
    deserialized_obj = json.loads(json_str)
    assert deserialized_obj == obj.model_dump()

def test_deserialize_heartbeat_throughput():
    json_str = '{"total_heartbeats": 100, "total_messages": 50}'
    obj = SwarmforgeSerializer.deserialize(json_str, HeartbeatThroughput)
    assert isinstance(obj, HeartbeatThroughput)
    assert obj.total_heartbeats == 100
    assert obj.total_messages == 50

def test_serialize_role_assignment_stats():
    obj = RoleAssignmentStats(total_assignments=100, successful_assignments=50)
    json_str = SwarmforgeSerializer.serialize(obj)
    deserialized_obj = json.loads(json_str)
    assert deserialized_obj == obj.model_dump()

def test_deserialize_role_assignment_stats():
    json_str = '{"total_assignments": 100, "successful_assignments": 50}'
    obj = SwarmforgeSerializer.deserialize(json_str, RoleAssignmentStats)
    assert isinstance(obj, RoleAssignmentStats)
    assert obj.total_assignments == 100
    assert obj.successful_assignments == 50

def test_serialize_swarm_state_machine():
    obj = SwarmStateMachine(current_state="IDLE", previous_state="ACTIVE")
    json_str = SwarmforgeSerializer.serialize(obj)
    deserialized_obj = json.loads(json_str)
    assert deserialized_obj == obj.model_dump()

def test_deserialize_swarm_state_machine():
    json_str = '{"current_state": "IDLE", "previous_state": "ACTIVE"}'
    obj = SwarmforgeSerializer.deserialize(json_str, SwarmStateMachine)
    assert isinstance(obj, SwarmStateMachine)
    assert obj.current_state == "IDLE"
    assert obj.previous_state == "ACTIVE"

def test_serialize_invalid_type():
    obj = "invalid type"
    with pytest.raises(TypeError):
        SwarmforgeSerializer.serialize(obj)

def test_deserialize_invalid_type():
    json_str = '{"key": "value"}'
    with pytest.raises(TypeError):
        SwarmforgeSerializer.deserialize(json_str, SwarmStateMachine)
