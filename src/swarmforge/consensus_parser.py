import argparse

def parse_consensus_args(args: list[str]) -> argparse.Namespace:
    """
    Parses command line arguments related to consensus.

    Args:
        args (list[str]): List of command line arguments.

    Returns:
        argparse.Namespace: Namespace containing consensus-related arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--consensus-type", help="Type of consensus algorithm to use.")
    parser.add_argument("--consensus-timeout", type=int, help="Timeout for consensus in seconds.")
    parser.add_argument("--consensus-retries", type=int, help="Number of retries for consensus.")

    return parser.parse_args(args)
