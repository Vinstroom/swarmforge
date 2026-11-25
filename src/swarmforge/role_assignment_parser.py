from typing import Dict, Any
import re

def parse_role_assignment(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse role assignment configuration data.

    Scores are expected to be in the format 'role1:0.5,role2:0.3,role3:0.2'.
    Agents are expected to be in the format 'agent1,agent2,agent3'.
    """
    role_scores = config_data.get('role_scores', '')
    agents = config_data.get('agents', '')

    role_scores_regex = re.compile(r'^(\w+:\d+(\.\d+)?)(\,\w+:\d+(\.\d+)?)*$')
    agents_regex = re.compile(r'^(\w+,)*\w+$')

    if not role_scores_regex.match(role_scores):
        raise ValueError("Invalid role scores format. Expected 'role1:0.5,role2:0.3,role3:0.2'")

    if not agents_regex.match(agents):
        raise ValueError("Invalid agents format. Expected 'agent1,agent2,agent3'")

    config_data['role_scores'] = {role: float(score) for role, score in [s.split(':') for s in role_scores.split(',')]}
    config_data['agents'] = agents.split(',')

    return config_data
