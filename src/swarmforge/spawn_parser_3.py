import argparse
import datetime
from typing import Optional

from swarmforge.timestamp import Timestamp

def parse_spawn_config(args: argparse.Namespace) -> dict:
    """Parse spawn config from command line arguments."""
    try:
        timestamp = Timestamp(datetime.datetime.fromisoformat(args.timestamp))
        return {
            "start_time": timestamp.timestamp,
            "duration": args.duration,
            "agent_count": args.agents,
            "role": args.role,
        }
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid timestamp format: {e}")

def main() -> None:
    """Parse command line arguments and print spawn config."""
    parser = argparse.ArgumentParser(description="Spawn swarm configuration.")
    parser.add_argument("-t", "--timestamp", required=True, help="Start time in ISO 8601 format")
    parser.add_argument("-d", "--duration", required=True, type=int, help="Duration in seconds")
    parser.add_argument("-a", "--agents", required=True, type=int, help="Number of agents")
    parser.add_argument("-r", "--role", required=True, help="Role for the swarm")

    args = parser.parse_args()

    config = parse_spawn_config(args)
    print(config)

if __name__ == "__main__":
    main()
