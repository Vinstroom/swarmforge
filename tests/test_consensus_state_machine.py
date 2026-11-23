import pytest
from src.swarmforge.consensus_state_machine import ConsensusStateMachine

def test_initial_state():
    sm = ConsensusStateMachine("init", lambda *args: None)
    assert sm.get_state() == "init"

def test_add_transition():
    sm = ConsensusStateMachine("init", lambda *args: None)
    sm.add_transition("init", "ready")
    assert sm.transitions == {"init": "ready"}

def test_process_no_transition():
    sm = ConsensusStateMachine("init", lambda *args: None)
    async with pytest.defer() as callback:
        sm.on_change = callback.callback
        await sm.process("event")
        assert sm.get_state() == "init"
        assert not callback.called

def test_process_transition():
    sm = ConsensusStateMachine("init", lambda *args: None)
    sm.add_transition("init", "ready")
    async with pytest.defer() as callback:
        sm.on_change = callback.callback
        await sm.process("event")
        assert sm.get_state() == "ready"
        assert callback.called_once_with("ready", "event")

def test_process_loop_transition():
    sm = ConsensusStateMachine("init", lambda *args: None)
    sm.add_transition("init", "ready")
    sm.add_transition("ready", "init")
    async with pytest.defer() as callback:
        sm.on_change = callback.callback
        await sm.process("event")
        await sm.process("event")
        assert sm.get_state() == "init"
        assert callback.call_count == 2
