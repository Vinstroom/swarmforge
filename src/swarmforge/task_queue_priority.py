"""Priority computation for task queue items.

Provides a pure function to compute a numeric priority value
from an optional priority string, suitable for ordering tasks.
"""

from __future__ import annotations

from typing import Optional


PRIORITY_MAP: dict[str, int] = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "background": 4,
}


def compute_priority(priority: Optional[str] = None) -> int:
    """Return a numeric priority for a given priority label.

    If *priority* is None or not recognised, defaults to *medium*.

    Args:
        priority: Optional priority label (case-insensitive).

    Returns:
        Integer priority where lower values indicate higher urgency.
    """
    if priority is None:
        return PRIORITY_MAP["medium"]
    return PRIORITY_MAP.get(priority.strip().lower(), PRIORITY_MAP["medium"])
