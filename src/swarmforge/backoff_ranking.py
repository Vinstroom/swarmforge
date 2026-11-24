import typing
from swarmforge.backoff_stats import BackoffStats, BackoffStat
from swarmforge.backoff_policies_and_metrics import BackoffPolicy

class BackoffRanker:
    """Rank backoff policies based on swarm-level metrics."""

    def __init__(self, backoff_stats: BackoffStats):
        self._backoff_stats = backoff_stats

    def rank_policies(self, policies: typing.Sequence[BackoffPolicy]) -> typing.Sequence[typing.Tuple[BackoffPolicy, float]]:
        """Rank backoff policies based on the total failure count.

        Args:
            policies (typing.Sequence[BackoffPolicy]): The list of backoff policies to rank.

        Returns:
            typing.Sequence[typing.Tuple[BackoffPolicy, float]]: A list of tuples, where each tuple contains a
                backoff policy and its rank as a score (0.0 - 1.0). Policies with lower failure counts receive
                higher scores.
        """
        failure_counts = {policy: self._backoff_stats.total_failed_count(policy) for policy in policies}
        rank_scores = {policy: 1.0 / (count + 1) for policy, count in failure_counts.items()}
        return sorted([(policy, score) for policy, score in rank_scores.items()], key=lambda x: x[1], reverse=True)
