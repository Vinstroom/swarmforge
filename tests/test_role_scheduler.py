import pytest
from datetime import datetime, timezone, timedelta
from src.swarmforge.role_scheduler import RoleScheduler, RoleWindow, RoleAssignmentStats

def test_add_window_no_overlap():
    scheduler = RoleScheduler()
    scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0))
    scheduler.add_window("role2", datetime(2022, 1, 1, 1, 0), datetime(2022, 1, 1, 2, 0))

def test_add_window_overlap():
    scheduler = RoleScheduler()
    with pytest.raises(ValueError) as e_info:
        scheduler.add_window("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0))
        scheduler.add_window("role2", datetime(2022, 1, 1, 0, 30), datetime(2022, 1, 1, 2, 0))

def test_active_role_single_window():
    scheduler = RoleScheduler(
        [
            RoleWindow("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0)),
        ]
    )
    assert scheduler.active_role() == "role1"

def test_active_role_no_window():
    scheduler = RoleScheduler()
    assert scheduler.active_role() is None

def test_next_role_change_single_window():
    scheduler = RoleScheduler(
        [
            RoleWindow("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0)),
        ]
    )
    assert scheduler.next_role_change() == datetime(2022, 1, 1, 1, 0)

def test_role_duration_left_active():
    scheduler = RoleScheduler(
        [
            RoleWindow("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0)),
        ]
    )
    assert scheduler.role_duration_left("role1") == 3600

def test_role_duration_left_inactive():
    scheduler = RoleScheduler()
    assert scheduler.role_duration_left("role1") is None

def test_rotate_if_due_no_change():
    scheduler = RoleScheduler(
        [
            RoleWindow("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0)),
        ]
    )
    scheduler.active_role()  # Seed active role
    assert scheduler.rotate_if_due() == "role1"

def test_get_stats():
    scheduler = RoleScheduler(
        [
            RoleWindow("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0)),
        ]
    )
    scheduler.active_role()  # Seed active role
    stats = scheduler.get_stats()
    assert stats.current_role == "role1"

def test_swarm_metrics():
    scheduler = RoleScheduler(
        [
            RoleWindow("role1", datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 1, 0)),
            RoleWindow("role2", datetime(2022, 1, 1, 0, 30), datetime(2022, 1, 1, 1, 30)),
        ]
    )
    scheduler.active_role()  # Seed active roles
    metrics = scheduler.swarm_metrics()
    assert metrics["active_roles"] == 2
