from typing import Dict, Any
import json
from .backoff_stats import BackoffStats
from .swarm_metrics import SwarmMetrics

class BackoffMetricsSerializer:
    """Helper class for serializing and deserializing backoff policies and swarm-level metrics."""

    @staticmethod
    def serialize_backoff_stats(backoff_stats: BackoffStats) -> str:
        """Serialize BackoffStats object to a JSON string."""
        return json.dumps(backoff_stats.__dict__)

    @staticmethod
    def deserialize_backoff_stats(serialized: str) -> BackoffStats:
        """Deserialize JSON string to a BackoffStats object."""
        data = json.loads(serialized)
        return BackoffStats(**data)

    @staticmethod
    def serialize_swarm_metrics(swarm_metrics: SwarmMetrics) -> str:
        """Serialize SwarmMetrics object to a JSON string."""
        return json.dumps(swarm_metrics.__dict__)

    @staticmethod
    def deserialize_swarm_metrics(serialized: str) -> SwarmMetrics:
        """Deserialize JSON string to a SwarmMetrics object."""
        data = json.loads(serialized)
        return SwarmMetrics(**data)

    @staticmethod
    def serialize_swarm_data(swarm_metrics: SwarmMetrics, backoff_stats: BackoffStats) -> Dict[str, Any]:
        """Serialize SwarmMetrics and BackoffStats objects to a single JSON string."""
        data = {
            'swarm_metrics': BackoffMetricsSerializer.serialize_swarm_metrics(swarm_metrics),
            'backoff_stats': BackoffMetricsSerializer.serialize_backoff_stats(backoff_stats)
        }
        return json.dumps(data)

    @staticmethod
    def deserialize_swarm_data(serialized: str) -> Dict[str, Any]:
        """Deserialize JSON string to a dictionary containing SwarmMetrics and BackoffStats objects."""
        data = json.loads(serialized)
        return {
            'swarm_metrics': BackoffMetricsSerializer.deserialize_swarm_metrics(data['swarm_metrics']),
            'backoff_stats': BackoffMetricsSerializer.deserialize_backoff_stats(data['backoff_stats'])
        }
