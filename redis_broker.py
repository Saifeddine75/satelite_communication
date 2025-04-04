# pipeline/redis_broker.py
import redis
import json
import logging
from typing import Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataPipeline")

class RedisBroker:
    def __init__(self, host="localhost", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        
    def publish_telemetry(self, modem_id: str, data: bytes):
        """Publish telemetry data to channel"""
        self.redis.publish(f"modem:{modem_id}:telemetry", data.hex())
        
    def publish_telecommand(self, modem_id: str, data: bytes):
        """Publish telecommand data to channel"""
        self.redis.publish(f"modem:{modem_id}:telecommand", data.hex())
        
    def subscribe_telemetry(self, modem_id: str, callback: Callable):
        """Subscribe to telemetry channel"""
        self.pubsub.subscribe(**{f"modem:{modem_id}:telemetry": callback})
        
    def subscribe_telecommand(self, modem_id: str, callback: Callable):
        """Subscribe to telecommand channel"""
        self.pubsub.subscribe(**{f"modem:{modem_id}:telecommand": callback})
        
    def cache_metrics(self, modem_id: str, metrics: dict, ttl: int = 30):
        """Cache metrics with time-to-live"""
        self.redis.setex(
            f"modem:{modem_id}:metrics",
            ttl,
            json.dumps(metrics)
        )
        
    def get_cached_metrics(self, modem_id: str) -> Optional[dict]:
        """Get cached metrics"""
        data = self.redis.get(f"modem:{modem_id}:metrics")
        return json.loads(data) if data else None
        
    def run(self):
        """Start listening for messages"""
        self.pubsub.run_in_thread(sleep_time=0.001)
        
    def close(self):
        """Cleanup resources"""
        self.pubsub.close()
        self.redis.close()