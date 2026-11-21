import time
from collections import Counter, deque
from typing import Dict, List, Optional

class ThroughputCalculator:
    def __init__(self, window_size: int = 60, interval: float = 1.0):
        self.window_size = window_size
        self.interval = interval
        self.window_start = time.time()
        self.event_counts: Counter = Counter()
        self.last_ticks: Optional[Dict[str, float]] = None

    def tick(self, event_type: str) -> None:
        now = time.time()
        if now - self.window_start > self.interval:
            self._reset_window()
        self.event_counts[event_type] += 1

    def calculate_throughput(self) -> Dict[str, float]:
        now = time.time()
        if now - self.window_start > self.interval:
            self._reset_window()
        counts = self.event_counts.copy()
        throughput = {event: count / (now - self.window_start) for event, count in counts.items()}
        if self.last_ticks is not None:
            throughput.update({event: (count - last) / (now - self.last_ticks[event])
                              for event, count in counts.items()
                              if event in self.last_ticks})
        self.last_ticks = throughput
        return throughput

    def _reset_window(self) -> None:
        self.window_start = time.time()
        self.event_counts.clear()
        self.last_ticks = None
