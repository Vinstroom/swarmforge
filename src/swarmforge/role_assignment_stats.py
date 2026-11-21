import collections
from typing import Dict, List, Optional

from swarmforge.role_scheduler import RoleAssignment

class RoleAssignmentStats:
    """Collect and provide statistics related to role assignment."""

    def __init__(self):
        self.role_assignments: List[RoleAssignment] = []
        self.role_counts: Dict[str, int] = collections.defaultdict(int)
        self.total_assignments = 0

    def update_stats(self, role_assignments: List[RoleAssignment]) -> None:
        """Updates the statistics with new role assignments."""
        for assignment in role_assignments:
            self.role_assignments.append(assignment)
            self.role_counts[assignment.role] += 1
            self.total_assignments += 1

    def get_role_assignment_counts(self) -> Dict[str, int]:
        """Returns a dict of role names and their counts."""
        return dict(self.role_counts)

    def get_total_assignments(self) -> int:
        """Returns the total number of role assignments."""
        return self.total_assignments

    def get_assignment_at(self, index: int) -> Optional[RoleAssignment]:
        """Returns the role assignment at the given index, or None if it doesn't exist."""
        return self.role_assignments[index] if 0 <= index < len(self.role_assignments) else None
