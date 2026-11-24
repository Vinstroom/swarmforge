import json
from typing import Any, Dict, List, Union

class SwarmFormatter:
    """Formats swarm data into a human-readable output."""

    def __init__(self, swarm_data: Dict[str, Any]):
        self.swarm_data = swarm_data

    def format_swarm(self) -> str:
        """Formats the swarm data into a human-readable string."""
        formatted_data: List[str] = []

        # Format bots/agents
        formatted_data.append(f"Bots/Agents ({len(self.swarm_data['bots'])}):")
        for bot in self.swarm_data['bots']:
            formatted_data.append(f"- {bot['name']}: {bot['role']} {self._get_bot_status(bot)}")

        # Format tasks
        formatted_data.append(f"\nTasks ({len(self.swarm_data['tasks'])}):")
        for task in self.swarm_data['tasks']:
            formatted_data.append(f"- {task['id']}: {task['status']} {self._get_task_time(task)}")

        # Format consensus metrics
        formatted_data.append(f"\nConsensus Metrics:")
        formatted_data.append(f"- Throughput: {self.swarm_data['consensus_metrics']['throughput']}")
        formatted_data.append(f"- Divergence: {self.swarm_data['consensus_metrics']['divergence']}")

        # Format heartbeat metrics
        formatted_data.append(f"\nHeartbeat Metrics:")
        formatted_data.append(f"- Throughput: {self.swarm_data['heartbeat_metrics']['throughput']}")

        return "\n".join(formatted_data)

    def _get_bot_status(self, bot: Dict[str, Any]) -> str:
        """Returns the status of a bot/agent as a string."""
        if bot['online']:
            return "online"
        else:
            return "offline"

    def _get_task_time(self, task: Dict[str, Any]) -> str:
        """Returns the start and end time of a task as a string."""
        if task['start_time'] and task['end_time']:
            return f"({task['start_time']} - {task['end_time']})"
        elif task['start_time']:
            return f"(start: {task['start_time']})"
        else:
            return ""
