import time
from collections import defaultdict
from typing import Dict, List, Optional
from swarmforge.message_bus import MessageBus, MessageBusEvent

class MessageBusMetrics:
    """Calculate metrics for a message bus."""

    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self._last_send_times: Dict[str, float] = defaultdict(float)
        self._last_receive_times: Dict[str, float] = defaultdict(float)

    def update_metrics(self, event: MessageBusEvent):
        if event.type == MessageBusEvent.Type.SENT:
            self._last_send_times[event.bot_id] = time.time()
        elif event.type == MessageBusEvent.Type.RECEIVED:
            self._last_receive_times[event.bot_id] = time.time()

    def get_ranking(self, bots: List[str]) -> List[float]:
        """Return a list of ranks for the given list of bots, based on message send/receive times."""
        ranks = []
        total_time = time.time() - min(self._last_send_times.values())
        for bot_id in bots:
            send_time = total_time - (time.time() - self._last_send_times[bot_id])
            receive_time = total_time - (time.time() - self._last_receive_times[bot_id])
            ranks.append((send_time + receive_time) / 2)
        ranks.sort()
        return [rank / sum(ranks) for rank in ranks]
