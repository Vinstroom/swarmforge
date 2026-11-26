"""
backoff_metrics.py

This module provides helper functions to calculate and retrieve metrics related to backoff policies
and swarm-level metrics.
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

from swarmforge.backoff_error import BackoffError
from swarmforge.backoff_helper import BackoffStrategy
from swarmforge.backoff_message_queue_state_machine import BackoffMessageQueueStateMachine
from swarmforge.backoff_strategy import BackoffStrategyType
from swarmforge.timestamp_utils import UtcTimestamp

class BackoffMetrics:
    """Calculates and stores metrics related to backoff policies and swarm-level metrics."""

    def __init__(self) -> None:
        self._backoff_counts: Dict[BackoffStrategyType, int] = defaultdict(int)
        self._last_backoff_time: Dict[BackoffStrategyType, UtcTimestamp] = defaultdict(UtcTimestamp)
        self._total_backoff_time: Dict[BackoffStrategyType, float] = defaultdict(float)

    def update_backoff_metrics(self, error: BackoffError) -> None:
        """Update metrics when a backoff error occurs."""
        strategy = error.backoff_strategy
        self._backoff_counts[strategy] += 1
        current_time = UtcTimestamp(datetime.utcnow())
        self._total_backoff_time[strategy] += (current_time - self._last_backoff_time[strategy]).total_seconds()
        self._last_backoff_time[strategy] = current_time

    def create_backoff_strategy_report(self) -> Dict[BackoffStrategyType, Dict[str, int or float]]:
        """Create a report of backoff strategy metrics."""
        return {
            strategy: {"count": count, "total_time_seconds": total_time}
            for strategy, count in self._backoff_counts.items()
            for total_time in sorted(self._total_backoff_time.values())
        }

    def calculate_average_backoff_time(self) -> Dict[BackoffStrategyType, float]:
        """Calculate the average backoff time for each strategy."""
        return {
            strategy: total_time / count
            for strategy, count in self._backoff_counts.items()
            if count > 0
            for total_time in self._total_backoff_time.values()
        }

    def calculate_swarm_level_metrics(
        self, active_agents: int, new_messages: int, resolved_messages: int
    ) -> Dict[str, Tuple[int, int, int, float]]:
        """Calculate swarm-level metrics."""
        total_messages = new_messages - resolved_messages
        average_message_rate = total_messages / (active_agents * (UtcTimestamp.utcnow() - self._last_backoff_time).total_seconds())
        return {
            "active_agents": (active_agents,),
            "new_messages": (new_messages,),
            "resolved_messages": (resolved_messages,),
            "average_message_rate": (average_message_rate,)
        }

def register_metrics(backoff_metrics: BackoffMetrics, state_machine: BackoffMessageQueueStateMachine) -> None:
    """Register to update backoff metrics when errors occur."""
    state_machine.register_error_callback(backoff_metrics.update_backoff_metrics)
