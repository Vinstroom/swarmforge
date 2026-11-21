import pytest
from swarmforge.scoreboard import Scoreboard, AgentPerformanceMetric
from swarmforge.timestamp import Timestamp
from swarmforge.role_scheduler import RoleScheduler


class FakeRole:
    def get_score_multiplier(self) -> int:
        return 5


class FakeRoleScheduler:
    def get_current_roles(self) -> dict:
        return {"agent_a": FakeRole(), "agent_b": FakeRole()}


def test_scoreboard_init():
    sb = Scoreboard()
    assert sb.scores == {}
    assert sb.ranks == []


def test_update_score():
    sb = Scoreboard()
    sb.update_score("a", 10)
    assert sb.scores["a"] == 10


def test_update_scores():
    sb = Scoreboard()
    sb.update_scores({"a": 5, "b": 3})
    assert sb.scores == {"a": 5, "b": 3}


def test_calculate_ranks():
    sb = Scoreboard()
    sb.update_scores({"alice": 30, "bob": 50, "carol": 20})
    sb.calculate_ranks()
    assert sb.ranks == ["bob", "alice", "carol"]


def test_get_rank():
    sb = Scoreboard()
    sb.update_scores({"x": 100, "y": 200})
    assert sb.get_rank("y") == 1
    assert sb.get_rank("x") == 2


def test_get_ranks():
    sb = Scoreboard()
    sb.update_scores({"z": 1, "w": 2})
    ranks = sb.get_ranks()
    assert ranks == {"w": 1, "z": 2}


def test_reset():
    sb = Scoreboard()
    sb.update_score("a", 10)
    sb.calculate_ranks()
    sb.reset()
    assert sb.scores == {}
    assert sb.ranks == []


def test_agent_performance_metric_calculate_scores_no_heartbeat():
    rs = FakeRoleScheduler()
    interval = Timestamp(10)
    apm = AgentPerformanceMetric(rs, interval)
    apm.calculate_scores()
    assert apm.scores.scores == {"agent_a": 0, "agent_b": 0}


def test_agent_performance_metric_calculate_scores_with_heartbeat():
    rs = FakeRoleScheduler()
    interval = Timestamp(10)
    apm = AgentPerformanceMetric(rs, interval)
    apm.update_heartbeats("agent_a", Timestamp(20))
    apm.calculate_scores()
    # 20 // 10 = 2, times multiplier 5 = 10
    assert apm.scores.scores == {"agent_a": 10}
    assert "agent_a" not in apm.last_heartbeats
