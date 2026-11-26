from collections import defaultdict
from typing import Dict, List, Tuple
from .backoff_validator import BackoffValidator
from .backoff_stats import BackoffStats

class BackoffMetrics:
    """Calculate and provide backoff metrics and ranking for swarms"""

    def __init__(self):
        self.backoff_stats: Dict[str, BackoffStats] = defaultdict(BackoffStats)
        self.backoff_validator = BackoffValidator()

    def update_stats(self, agent_id: str, backoff_info: dict):
        """Update backoff statistics for an agent"""
        self.backoff_stats[agent_id].update(backoff_info)

    def calculate_ranking(self) -> List[Tuple[str, int]]:
        """Calculate and return a ranking of agents based on their backoff performance"""
        ranks: Dict[str, int] = {agent_id: self.backoff_stats[agent_id].performance_score() for agent_id in self.backoff_stats}

        # Sort agents by performance score in descending order
        sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)

        # Assign ranks
        rank = 1
        for agent_id, score in sorted_ranks:
            ranks[agent_id] = rank
            rank += 1

        return sorted_ranks

    def performance_score(self, agent_id: str) -> int:
        """Return the performance score for an agent"""
        return self.backoff_stats[agent_id].performance_score()
