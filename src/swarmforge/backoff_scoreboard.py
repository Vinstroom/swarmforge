from collections import defaultdict
from typing import Dict, List, Optional

from .backoff_helper import BackoffHelper
from .backoff_policies_and_metrics import BackoffPolicy
from .consensus_metrics import SwarmMetrics
from .heartbeat_throughput import HeartbeatThroughput

class BackoffScoreboard:
    """Calculates and maintains backoff scores for swarm bots based on policies and metrics."""

    def __init__(self, backoff_helper: BackoffHelper, metrics: SwarmMetrics, heartbeat_throughput: HeartbeatThroughput):
        self.backoff_helper = backoff_helper
        self.metrics = metrics
        self.heartbeat_throughput = heartbeat_throughput
        self.backoff_scores: Dict[str, float] = defaultdict(float)
        self.backoff_policies: Dict[str, BackoffPolicy] = {}

    def register_policy(self, bot_id: str, backoff_policy: BackoffPolicy) -> None:
        """Register a backoff policy for a bot."""
        self.backoff_policies[bot_id] = backoff_policy

    def update_scores(self) -> None:
        """Update backoff scores based on current metrics and policies."""
        for bot_id, backoff_policy in self.backoff_policies.items():
            self.backoff_scores[bot_id] = self.calculate_score(bot_id, backoff_policy)

    def calculate_score(self, bot_id: str, backoff_policy: BackoffPolicy) -> float:
        """Calculate a backoff score for a bot based on its policy and current swarm metrics."""
        # Note: Policy might dictate use of different metrics, e.g., failed tasks, consensus divergence, etc.
        failed_tasks = self.metrics.get_failed_tasks(bot_id)
        successful_tasks = self.metrics.get_successful_tasks(bot_id)
        consensus_divergence = self.metrics.get_consensus_divergence(bot_id)
        heartbeat_throughput = self.heartbeat_throughput.get_heartbeat_throughput(bot_id)

        return backoff_policy.score(
            failed_tasks=failed_tasks,
            successful_tasks=successful_tasks,
            consensus_divergence=consensus_divergence,
            heartbeat_throughput=heartbeat_throughput
        )
