import pytest
from swarmforge.spawn_parser import parse_spawn_command, SpawnCommand

def test_parse_spawn_command_valid():
    command = "spawn worker --count 3 --role processor --ttl 60"
    result = parse_spawn_command(command)
    assert result == SpawnCommand(agent_type="worker", count=3, role="processor", ttl=60)

def test_parse_spawn_command_missing_agent_type():
    command = "spawn"
    with pytest.raises(ValueError, match="Missing agent type"):
        parse_spawn_command(command)

def test_parse_spawn_command_invalid_count():
    command = "spawn worker --count zero"
    with pytest.raises(ValueError, match="Invalid --count value: 'zero'"):
        parse_spawn_command(command)

def test_parse_spawn_command_missing_count_value():
    command = "spawn worker --count"
    with pytest.raises(ValueError, match="Missing value for --count"):
        parse_spawn_command(command)

def test_parse_spawn_command_unknown_flag():
    command = "spawn worker --unknown"
    with pytest.raises(ValueError, match="Unknown flag: 'unknown'"):
        parse_spawn_command(command)

def test_parse_spawn_command_empty():
    command = ""
    with pytest.raises(ValueError, match="Empty command"):
        parse_spawn_command(command)
