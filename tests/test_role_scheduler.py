import pytest
from datetime import datetime, timedelta, timezone
from src.swarmforge.role_scheduler import RoleScheduler, RoleWindow, RoleAssignmentStats

def test_add_window_overlapping():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        scheduler.add_window("role2", datetime(2022, 1, 1, 0, 30, 0, tzinfo=timezone.utc),
                             datetime(2022, 1, 1, 0, 45, 0, tzinfo=timezone.utc))

def test_active_role():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    scheduler.add_window("role2", datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 2, 0, 0, tzinfo=timezone.utc))
    assert scheduler.active_role() == "role1"
    scheduler._now_fn = lambda: datetime(2022, 1, 1, 1, 30, 0, tzinfo=timezone.utc)
    assert scheduler.active_role() == "role2"

def test_next_role_change():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    scheduler.add_window("role2", datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 2, 0, 0, tzinfo=timezone.utc))
    assert scheduler.next_role_change() == datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc)

def test_role_duration_left():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    scheduler._now_fn = lambda: datetime(2022, 1, 1, 0, 30, 0, tzinfo=timezone.utc)
    assert scheduler.role_duration_left("role1") == 30 * 60

def test_rotate_if_due():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    scheduler.add_window("role2", datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 2, 0, 0, tzinfo=timezone.utc))
    assert scheduler.rotate_if_due() == "role2"
    scheduler._now_fn = lambda: datetime(2022, 1, 1, 1, 30, 0, tzinfo=timezone.utc)
    assert scheduler.rotate_if_due() == None

def test_get_stats():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    scheduler._now_fn = lambda: datetime(2022, 1, 1, 0, 30, 0, tzinfo=timezone.utc)
    scheduler.active_role()
    stats = scheduler.get_stats()
    assert stats.total_assignments == 1
    assert stats.current_role == "role1"
    assert stats.current_role_duration > 0

def test_swarm_metrics():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    scheduler.add_window("role2", datetime(2022, 1, 1, 1, 0, 0, tzinfo=timezone.utc),
                         datetime(2022, 1, 1, 2, 0, 0, tzinfo=timezone.utc))
    scheduler._now_fn = lambda: datetime(2022, 1, 1, 0, 30, 0, tzinfo=timezone.utc)
    scheduler.active_role()
    metrics = scheduler.swarm_metrics()
    assert metrics["active_roles"] == 1
    assert metrics["total_windows"] == 2
    assert metrics["active_ratio"] == 0.5
    assert metrics["role_transitions"] == 0
