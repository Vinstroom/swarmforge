import heapq
from typing import List, Dict

def calculate_score(agent: Dict[str, int], metrics: Dict[str, int]) -> int:
    """Calculate agent's score based on given metrics."""
    score = 0
    for metric, weight in metrics.items():
        score += agent.get(metric, 0) * weight
    return score

def rank_agents(agents: List[Dict[str, int]], metrics: Dict[str, int]) -> List[Dict[str, int]]:
    """Rank agents based on their scores using given metrics."""
    # Calculate scores for each agent
    scored_agents = [(calculate_score(agent, metrics), agent) for agent in agents]

    # Heapify the list of tuples based on the scores in reverse order
    heapq.heapify(scored_agents)

    # Convert the heap back to a list and reverse it to get the ranking in descending order
    ranked_agents = [ährung for _, agent in heapq.nsmallest(len(scored_agents), scored_agents)]

    return ranked_agents
