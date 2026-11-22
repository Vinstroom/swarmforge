from collections import defaultdict
from typing import Dict, List, Tuple

from swarmforge.backoff_error import BackoffError
from swarmforge.backoff_policies_and_metrics import BackoffPolicy, BackoffMetric

def calculate_backoff_stats(backoff_errors: List[BackoffError]) -> Dict[BackoffPolicy, Tuple[int, int, float]]:
    """Calculate backoff statistics for each policy.

    Args:
        backoff_errors (List[BackoffError]): List of backoff errors.

    Returns:
        Dict[BackoffPolicy, Tuple[int, int, float]]: Dictionary containing policy as key and tuple of total retries,
        max retries, and average retries as value.
    """
    stats = defaultdict(lambda: (0, 0, 0.0))

    for error in backoff_errors:
        policy = error.policy
        retry_count = error.retry_count

        stats[policy][0] += retry_count  # Total retries
        stats[policy][1] = max(stats[policy][1], retry_count)  # Max retries

    # Calculate average retries
    for policy, (total_retries, max_retries, _) in stats.items():
        stats[policy] = (total_retries, max_retries, total_retries / len(backoff_errors) if backoff_errors else 0)

    return {BackoffMetric.POLICY: policy for policy, (total_retries, max_retries, avg_retries) in stats.items()}
