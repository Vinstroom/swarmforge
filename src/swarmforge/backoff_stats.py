from collections import defaultdict
from typing import Dict, List, Tuple

from swarmforge.backoff_error import BackoffError
from swarmforge.backoff_policies_and_metrics import BackoffPolicy, BackoffMetric

def calculate_backoff_stats(backoff_errors: List[BackoffError], successful_requests: int) -> Dict[BackoffPolicy, Tuple[int, int, float, float]]:
    """Calculate backoff statistics for each policy, including rate of successful requests.

    Args:
        backoff_errors (List[BackoffError]): List of backoff errors.
        successful_requests (int): Number of successful requests in the same period.

    Returns:
        Dict[BackoffPolicy, Tuple[int, int, float, float]]: Dictionary containing policy as key and tuple of total retries,
        max retries, average retries, and successful requests rate as value.
    """
    stats = defaultdict(lambda: (0, 0, 0.0, 0.0))

    for error in backoff_errors:
        policy = error.policy
        retry_count = error.retry_count

        stats[policy][0] += retry_count  # Total retries
        stats[policy][1] = max(stats[policy][1], retry_count)  # Max retries

    # Calculate average retries and successful requests rate
    for policy, (total_retries, max_retries, _) in stats.items():
        stats[policy] = (total_retries, max_retries, total_retries / len(backoff_errors) if backoff_errors else 0, successful_requests / len(backoff_errors) if backoff_errors else 0)

    return {BackoffMetric.POLICY: policy for policy, (total_retries, max_retries, avg_retries, success_rate) in stats.items()}
