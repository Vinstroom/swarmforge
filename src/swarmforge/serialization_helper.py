from typing import Dict, Union
import json
from swarmforge.backoff_policies_and_metrics import BackoffPoliciesAndMetrics
from swarmforge.consensus_metrics import ConsensusMetrics
from swarmforge.heartbeat_throughput import HeartbeatThroughput
from swarmforge.role_assignment_stats import RoleAssignmentStats
from swarmforge.swarm_state_machine import SwarmStateMachine

class SwarmforgeSerializer:
    """Helper for serializing and deserializing swarmforge objects to/from JSON."""

    @staticmethod
    def serialize(obj: Union[BackoffPoliciesAndMetrics, ConsensusMetrics, HeartbeatThroughput,
                            RoleAssignmentStats, SwarmStateMachine]) -> str:
        """Serialize a swarmforge object to a JSON string."""
        if isinstance(obj, BackoffPoliciesAndMetrics):
            return json.dumps(obj.model_dump())
        elif isinstance(obj, ConsensusMetrics):
            return json.dumps(obj.model_dump())
        elif isinstance(obj, HeartbeatThroughput):
            return json.dumps(obj.model_dump())
        elif isinstance(obj, RoleAssignmentStats):
            return json.dumps(obj.model_dump())
        elif isinstance(obj, SwarmStateMachine):
            return json.dumps(obj.model_dump())
        else:
            raise TypeError(f"Unsupported object type: {type(obj).__name__}")

    @staticmethod
    def deserialize(json_str: str, obj_type: type) -> Union[BackoffPoliciesAndMetrics,
                                                          ConsensusMetrics, HeartbeatThroughput,
                                                          RoleAssignmentStats, SwarmStateMachine]:
        """Deserialize a JSON string to a swarmforge object."""
        obj_dict = json.loads(json_str)
        if obj_type == BackoffPoliciesAndMetrics:
            return BackoffPoliciesAndMetrics(**obj_dict)
        elif obj_type == ConsensusMetrics:
            return ConsensusMetrics(**obj_dict)
        elif obj_type == HeartbeatThroughput:
            return HeartbeatThroughput(**obj_dict)
        elif obj_type == RoleAssignmentStats:
            return RoleAssignmentStats(**obj_dict)
        elif obj_type == SwarmStateMachine:
            return SwarmStateMachine(**obj_dict)
        else:
            raise TypeError(f"Unsupported object type: {obj_type.__name__}")
