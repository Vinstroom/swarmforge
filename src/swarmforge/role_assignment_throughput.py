from typing import Dict, List
from collections import defaultdict
import time

class RoleAssignmentThroughput:
    """Calculate throughput for role assignment."""

    def __init__(self):
        self._role_assignments: Dict[str, List[float]] = defaultdict(list)
        self._last_reset: Dict[str, float] = defaultdict(float)

    def record_assignment(self, role: str, timestamp: float) -> None:
        """Record a role assignment and update throughput."""
        self._role_assignments[role].append(timestamp)
        self._update_throughput(role)

    def _update_throughput(self, role: str) -> None:
        """Update and return the throughput for the given role."""
        now = time.monotonic()
        if now - self._last_reset[role] > 1.0:  # 1 second window
            self._last_reset[role] = now
            assignments = self._role_assignments[role]
            throughput = len(assignments) / (now - assignments[0])
            self._role_assignments[role] = []  # Clear assignments for this window
            return throughput

    def get_throughput(self) -> Dict[str, float]:
        """Return the current throughput for each role."""
        return {role: self._update_throughput(role) for role in self._role_assignments}
