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
        
    def run(self):
        """Start listening for messages"""
        self.pubsub.run_in_thread(sleep_time=0.001)
        
    def close(self):
        """Cleanup resources"""
        self.pubsub.close()
        self.redis.close()