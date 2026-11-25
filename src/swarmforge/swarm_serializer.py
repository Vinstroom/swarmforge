"""Helper for serializing backoff policies and swarm-level metrics."""

import json
from typing import Dict, Any
from .backoff_policies_and_metrics import (
    BackoffPolicy,
    Metrics,
    SwarmMetrics,
)

class SwarmSerializer:
    """Serializer for backoff policies and swarm-level metrics."""

    @staticmethod
    def serialize_backoff_policy(backoff_policy: BackoffPolicy) -> str:
        """Serialize a backoff policy to a JSON string."""
        return json.dumps(backoff_policy._asdict())

    @staticmethod
    def deserialize_backoff_policy(serialized_policy: str) -> BackoffPolicy:
        """Deserialize a backoff policy from a JSON string."""
        return BackoffPolicy(**json.loads(serialized_policy))

    @staticmethod
    def serialize_swarm_metrics(swarm_metrics: SwarmMetrics) -> str:
        """Serialize swarm-level metrics to a JSON string."""
        return json.dumps(swarm_metrics._asdict())

    @staticmethod
    def deserialize_swarm_metrics(serialized_metrics: str) -> SwarmMetrics:
        """Deserialize swarm-level metrics from a JSON string."""
        return SwarmMetrics(**json.loads(serialized_metrics))
