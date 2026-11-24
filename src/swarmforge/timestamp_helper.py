import datetime

class TimestampHelper:
    """Helper class to generate and parse timestamps."""

    @staticmethod
    def generate_timestamp() -> str:
        """Generate a timestamp string in ISO 8601 format."""
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    @staticmethod
    def parse_timestamp(ts: str) -> datetime.datetime:
        """Parse a timestamp string in ISO 8601 format and return a datetime object."""
        return datetime.datetime.fromisoformat(ts)
