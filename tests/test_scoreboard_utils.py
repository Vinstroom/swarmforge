import pytest
from src.swarmforge.scoreboard_utils import calculate_score, rank_agents

def test_calculate_score():
    agent = {"metric1": 5, "metric2": 3}
    metrics = {"metric1": 2, "metric2": 3}
    assert calculate_score(agent, metrics) == 13

def test_calculate_score_ignores_unknown_metrics():
    agent = {"metric1": 5, "metric2": 3}
    metrics = {"metric3": 2}
    assert calculate_score(agent, metrics) == 0

def test_rank_agents():
    agents = [{"metric1": 5, "metric2": 3}, {"metric1": 3, "metric2": 5}]
    metrics = {"metric1": 2, "metric2": 3}
    assert rank_agents(agents, metrics) == [{"metric1": 5, "metric2": 3}, {"metric1": 3, "metric2": 5}]
