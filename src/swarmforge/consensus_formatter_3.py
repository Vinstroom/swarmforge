from typing import List, Dict

from swarmforge.backoff_validator import BackoffValidator
from swarmforge.consensus_stats import ConsensusStats
from swarmforge.string_normalizer import StringNormalizer

class ConsensusFormatter:
    """Formatter for human-readable output of consensus-related metrics."""

    def __init__(self, backoff_validator: BackoffValidator, string_normalizer: StringNormalizer):
        self._backoff_validator = backoff_validator
        self._string_normalizer = string_normalizer

    def format_consensus_stats(self, stats: ConsensusStats) -> str:
        """Format consensus-related stats for human-readable output."""
        normalized_messages = self._string_normalizer.normalize(stats.messages)
        backoff_validated = self._backoff_validator.validate_messages(normalized_messages)

        result = f"Consensus Stats:\n"
        result += f"  Messages: {len(normalized_messages)}\n"
        result += f"  Backoff Validated: {backoff_validated}\n"
        result += f"  Consensus Duration: {stats.duration_seconds:.2f} seconds\n"
        result += f"  Throughput: {stats.throughput:.2f} messages/second"

        return result

    def format_consensus_divergence(self, divergences: List[Dict[str, str]]) -> str:
        """Format consensus divergence metrics for human-readable output."""
        normalized_divergences = [self._string_normalizer.normalize(div) for div in divergences]

        result = "Consensus Divergence:\n"
        for i, divergence in enumerate(normalized_divergences, start=1):
            result += f"  {i}. {divergence['source']} -> {divergence['destination']}\n"

        return result
