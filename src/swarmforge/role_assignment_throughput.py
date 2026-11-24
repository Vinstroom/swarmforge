import time
from typing import Dict, List

class RoleAssignmentThroughput:
    def __init__(self):
        self.start_time: float = time.time()
        self.role_assignments: Dict[str, List[float]] = {}

    def record_assignment(self, role: str, assignment_time: float) -> None:
        if role not in self.role_assignments:
            self.role_assignments[role] = []
        self.role_assignments[role].append(assignment_time)

    def calculate_throughput(self) -> Dict[str, float]:
        elapsed_time = time.time() - self.start_time
        return {role: len(assignments) / elapsed_time for role, assignments in self.role_assignments.items()}
