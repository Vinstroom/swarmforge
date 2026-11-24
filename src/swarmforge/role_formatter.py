"""Human-readable formatting for role assignment snapshots."""

from __future__ import annotations

import datetime
from typing import Sequence


class RoleFormatter:
    """Produce human-readable strings from role assignment data."""

    @staticmethod
    def format_assignment(
        agent_id: str,
        role: str,
        assigned_at: float,
    ) -> str:
        """Return a one-line summary of a single role assignment."""
        return f"[{datetime.datetime.fromtimestamp(assigned_at, tz=datetime.timezone.utc):%Y-%m-%dT%H:%M:%SZ}] Agent '{agent_id}' assigned role '{role}'"

    @staticmethod
    def format_table(
        agent_ids: Sequence[str],
        roles: Sequence[str],
        assigned_times: Sequence[float],
        title: str = "Role Assignment Snapshot",
    ) -> str:
        """Return a table of role assignments with aligned columns."""
        if not agent_ids:
            return f"{title} (empty)"

        lines: list[str] = [title, "=" * len(title)]
        header = f"{'Agent ID':<24} {'Role':<20} {'Assigned At (UTC)'}"
        lines.append(header)
        lines.append("-" * len(header))
        for agent_id, role, assigned_time in zip(agent_ids, roles, assigned_times):
            lines.append(f"{agent_id:<24} {role:<20} {datetime.datetime.fromtimestamp(assigned_time, tz=datetime.timezone.utc)}")
        return "\n".join(lines)

    @staticmethod
    def format_summary(
        role_counts: dict[str, int],
        total_agents: int,
    ) -> str:
        """Return a summary of role distribution."""
        parts = [f"Role Distribution (total agents: {total_agents})"]
        parts.append("-" * 40)
        for role, count in sorted(role_counts.items()):
            percentage = (count / total_agents * 100) if total_agents else 0.0
            parts.append(f"  {role:<20} {count:>4} ({percentage:5.1f}%)")
        return "\n".join(parts)
