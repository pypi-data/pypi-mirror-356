import json
import threading
from typing import Callable, Dict, Any

from .redis_connector import RedisConnector


class NeuralBridge:
    """Cross-instance communication via Redis Pub/Sub with offline fallback."""

    def __init__(self, redis: RedisConnector = None):
        self.redis = redis or RedisConnector()
        self.handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {}
        self.local_queue = []  # used when offline

    def publish(self, channel: str, message: Dict[str, Any]):
        """Publish a message on a channel."""
        payload = json.dumps(message)
        if self.redis.offline:
            self.local_queue.append((channel, message))
            if channel in self.handlers:
                self.handlers[channel](message)
        else:
            self.redis.client.publish(channel, payload)

    def subscribe(self, channel: str, handler: Callable[[Dict[str, Any]], None]):
        """Subscribe to a channel with a handler function."""
        self.handlers[channel] = handler
        if self.redis.offline:
            # deliver any queued messages for this channel
            for ch, msg in list(self.local_queue):
                if ch == channel:
                    handler(msg)
        else:
            thread = threading.Thread(target=self._listen, args=(channel, handler), daemon=True)
            thread.start()

    def _listen(self, channel: str, handler: Callable[[Dict[str, Any]], None]):
        pubsub = self.redis.client.pubsub()
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            if message['type'] != 'message':
                continue
            data = json.loads(message['data'])
            handler(data)

    # Convenience wrappers for common channels
    def publish_capability(self, capability: Dict[str, Any]):
        self.publish('channel:capabilities:new', capability)

    def publish_handoff(self, handoff: Dict[str, Any]):
        self.publish('channel:agent:handoff', handoff)

    def publish_result(self, result: Dict[str, Any]):
        self.publish('channel:agent:result', result)
