from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
from src.swarmforge.task_queue import TaskQueue

class TaskQueueState(ABC):
    @abstractmethod
    def transition(self, task_queue: TaskQueue) -> None:
        pass

class TaskQueueStateMachine:
    def __init__(self):
        self.states: Dict[str, TaskQueueState] = {}
        self.current_state: str = None

    def add_state(self, name: str, state: TaskQueueState) -> None:
        self.states[name] = state
        if not self.current_state:
            self.current_state = name

    def transition_to(self, state_name: str) -> None:
        if state_name in self.states:
            self.current_state = state_name
        else:
            raise ValueError(f"Unknown state: {state_name}")

    def process(self, task_queue: TaskQueue) -> None:
        if self.current_state:
            self.states[self.current_state].transition(task_queue)

# Example usage
class IdleState(TaskQueueState):
    def transition(self, task_queue: TaskQueue) -> None:
        # Implement idle state behavior
        pass

class WorkingState(TaskQueueState):
    def transition(self, task_queue: TaskQueue) -> None:
        # Implement working state behavior
        pass

task_queue_sm = TaskQueueStateMachine()
task_queue_sm.add_state("idle", IdleState())
task_queue_sm.add_state("working", WorkingState())
task_queue_sm.transition_to("working")
task_queue_sm.process(TaskQueue())
