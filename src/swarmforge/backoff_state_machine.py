from typing import Dict, Any
from src.swarmforge.backoff_policies_and_metrics import BackoffPolicies, BackoffMetrics
from src.swarmforge.backoff_strategy import BackoffStrategy


class BackoffStateMachine:
    """State machine for managing backoff policies and metrics."""

    def __init__(self, policies: BackoffPolicies, metrics: BackoffMetrics, strategy: BackoffStrategy):
        self._policies = policies
        self._metrics = metrics
        self._strategy = strategy
        self._current_state = 'active'

    def process_error(self, error: Exception) -> None:
        """Process error and update state based on backoff strategy."""
        self._metricsErrors.append(error)
        self._update_state()

    def _update_state(self) -> None:
        """Update state based on backoff strategy and metrics."""
        if self._metrics.error_count > self._policies.max_consecutive_errors and self._current_state != 'backoff':
            self._current_state = 'backoff'
            self._strategy.backoff()
        elif self._metrics.error_count == 0 and self._current_state != 'active':
            self._current_state = 'active'
            self._strategy.activate()
