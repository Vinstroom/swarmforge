from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from swarmforge.policies.backoff import BackoffPolicy
from swarmforge.metrics import SwarmMetric

import swarmforge.timestamp as ts

class RoleState(Enum):
    UNINIT = "UNINIT"
    ASSIGNED = "ASSIGNED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class RoleStateMachine(ABC):
    @abstractmethod
    def __init__(self, role: str, backoff_policy: BackoffPolicy, swarm_metrics: Optional[SwarmMetric] = None):
        if not isinstance(backoff_policy, BackoffPolicy):
            raise TypeError("backoff_policy must be an instance of BackoffPolicy")
        if swarm_metrics and not isinstance(swarm_metrics, SwarmMetric):
            raise TypeError("swarm_metrics must be an instance of SwarmMetric or None")
        self._role = role
        self._state = RoleState.UNINIT
        self._backoff_policy = backoff_policy
        self._swarm_metrics = swarm_metrics

    @property
    def role(self) -> str:
        return self._role

    @property
    def state(self) -> RoleState:
        return self._state

    @abstractmethod
    def assign_role(self) -> None:
        pass

    @abstractmethod
    def activate_role(self) -> None:
        pass

    @abstractmethod
    def deactivate_role(self) -> None:
        pass

    @abstractmethod
    def status(self) -> str:
        pass

    def backoff(self) -> None:
        self._backoff_policy.backoff()

    def update_metrics(self, metric: str, value: float) -> None:
        if self._swarm_metrics:
            self._swarm_metrics.update(metric, value)

@dataclass
class SimpleRoleStateMachine(RoleStateMachine):
    def __init__(self, role: str, backoff_policy: BackoffPolicy, swarm_metrics: Optional[SwarmMetric] = None):
        super().__init__(role, backoff_policy, swarm_metrics)

    def assign_role(self) -> None:
        self._state = RoleState.ASSIGNED

    def activate_role(self) -> None:
        self._state = RoleState.ACTIVE

    def deactivate_role(self) -> None:
        self._state = RoleState.INACTIVE

    def status(self) -> str:
        return f"{self._role}: {self._state.value} at {ts.now()}"
