import redis
import json
import logging
from typing import Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataPipeline")

class Redis:
    def __init__(self, host="localhost", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        
    def publish_telemetry(self, modem_id: str, data: bytes):
        """Publish telemetry data to channel"""
        self.redis.publish(f"modem:{modem_id}:telemetry", data.hex())

    def subscribe_telemetry(self, modem_id: str, callback: Callable):
        """Subscribe to telemetry channel"""
        self.pubsub.subscribe(**{f"modem:{modem_id}:telemetry": callback})
        
    def run(self):
        """Start listening for messages"""
        self.pubsub.run_in_thread()
        
    def close(self):
        """Cleanup resources"""
        self.pubsub.close()
        self.redis.close()