"""Compact ledger tracking role assignments and transitions for swarm agents."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class RoleEntry:
    """A single role assignment entry with metadata."""
    role: str
    agent_id: str
    assigned_at: float
    revoked_at: Optional[float] = None

    @property
    def is_active(self) -> bool:
        """Return True if the role is currently assigned."""
        return self.revoked_at is None

    @property
    def duration(self) -> Optional[float]:
        """Return the duration of the assignment in seconds, or None if active."""
        if self.revoked_at is None:
            return None
        return self.revoked_at - self.assigned_at


class RoleLedger:
    """A compact ledger tracking role assignments and transitions for swarm agents.

    Provides efficient lookups of current assignments, historical transitions,
    and aggregated statistics per role or agent.
    """

    def __init__(self) -> None:
        self._entries: List[RoleEntry] = []
        self._active: Dict[str, RoleEntry] = {}  # agent_id -> active entry

    def assign(self, role: str, agent_id: str, timestamp: Optional[float] = None) -> None:
        """Assign a role to an agent at an optional timestamp (defaults to now)."""
        if agent_id in self._active:
            raise ValueError(f"Agent {agent_id} already has an active role: {self._active[agent_id].role}")
        ts = timestamp if timestamp is not None else time.time()
        entry = RoleEntry(role=role, agent_id=agent_id, assigned_at=ts)
        self._entries.append(entry)
        self._active[agent_id] = entry

    def revoke(self, agent_id: str, timestamp: Optional[float] = None) -> None:
        """Revoke the current role of an agent at an optional timestamp."""
        entry = self._active.pop(agent_id, None)
        if entry is None:
            raise ValueError(f"Agent {agent_id} has no active role to revoke")
        entry.revoked_at = timestamp if timestamp is not None else time.time()

    def active_role(self, agent_id: str) -> Optional[str]:
        """Return the active role of an agent, or None."""
        entry = self._active.get(agent_id)
        return entry.role if entry else None

    def is_active(self, agent_id: str) -> bool:
        """Return True if the agent currently holds a role."""
        return agent_id in self._active

    def history(self, agent_id: Optional[str] = None, role: Optional[str] = None) -> List[RoleEntry]:
        """Return all entries filtered by optional agent_id and/or role."""
        result = self._entries
        if agent_id is not None:
            result = [e for e in result if e.agent_id == agent_id]
        if role is not None:
            result = [e for e in result if e.role == role]
        return result

    def active_agents_for_role(self, role: str) -> List[str]:
        """Return all agents currently assigned to the given role."""
        return [e.agent_id for e in self._active.values() if e.role == role]

    def roles_for_agent(self, agent_id: str) -> List[str]:
        """Return all roles ever held by an agent, in order of assignment."""
        return [e.role for e in self._entries if e.agent_id == agent_id]

    def transition_count(self, agent_id: Optional[str] = None) -> int:
        """Return the number of role transitions (assignments) for an agent or all."""
        if agent_id is not None:
            return sum(1 for e in self._entries if e.agent_id == agent_id)
        return len(self._entries)

    def stats(self) -> Dict[str, object]:
        """Return aggregated statistics about the ledger."""
        total_assignments = len(self._entries)
        active_count = len(self._active)
        unique_agents = len({e.agent_id for e in self._entries})
        unique_roles = len({e.role for e in self._entries})
        return {
            "total_assignments": total_assignments,
            "active_assignments": active_count,
            "unique_agents": unique_agents,
            "unique_roles": unique_roles,
        }

    def clear(self) -> None:
        """Remove all entries from the ledger."""
        self._entries.clear()
        self._active.clear()
