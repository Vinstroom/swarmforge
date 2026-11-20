import pytest
from swarmforge.timestamp import UnixTimestamp
from src.swarmforge.heartbeat_validator_2 import validate_heartbeat_interval, validate_heartbeat_timestamp

def test_validate_heartbeat_interval():
    assert validate_heartbeat_interval(0.4) == "Heartbeat interval must be at least 0.5 seconds."
    assert validate_heartbeat_interval(61) == "Heartbeat interval must be no more than 60 seconds."
    assert validate_heartbeat_interval(0.5) == validate_heartbeat_interval(60) == None

def test_validate_heartbeat_interval_custom_thresholds():
    assert validate_heartbeat_interval(0.4, 0.45, 65) == "Heartbeat interval must be at least 0.45 seconds."
    assert validate_heartbeat_interval(65, 0.45, 65) == "Heartbeat interval must be no more than 65 seconds."

def test_validate_heartbeat_timestamp():
    assert validate_heartbeat_timestamp(UnixTimestamp.now() + 1) == "Heartbeat timestamp cannot be in the future."
    assert validate_heartbeat_timestamp(UnixTimestamp.now() - 1) == None

def test_validate_heartbeat_timestamp_current_time():
    current_time = UnixTimestamp.now()
    assert validate_heartbeat_timestamp(current_time) == None
    assert validate_heartbeat_timestamp(current_time - 1) == None
