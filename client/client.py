# client_computer.py
import asyncio
import aiohttp
import logging
import aiohttp
from typing import Optional
from datetime import datetime
import redis
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ClientComputer")

class ClientComputer:
    def __init__(self, modem_id: str, redis_host="localhost"):
        self.modem_id = modem_id
        self.redis = redis.Redis(host=redis_host, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.running = False
        
    async def send_telecommand(self, data: bytes):
        """Send telecommand to modem via pipeline"""
        self.redis.publish(f"modem:{self.modem_id}:telecommand", data.hex())
        logger.info(f"Sent telecommand: {data.hex()}")
            
    async def monitor_metrics(self, interval=5):
        """Periodically fetch and log metrics"""
        metric_endpoints = [
            'status',
            'signal_strength',
            'bit_error_rate',
            'statistics'
        ]
        
        async with aiohttp.ClientSession() as session:
            while self.running:
                for endpoint in metric_endpoints:
                    try:
                        url = f"http://127.0.0.1:8000/metrics/{endpoint}"
                        async with session.get(url) as resp:
                            data = await resp.json()
                            self.logger.info(f"Metric {endpoint}: {data}")
                    except Exception as e:
                        self.logger.error(f"Failed to get metric {endpoint}: {e}")
                
                await asyncio.sleep(interval)
                
    async def run(self):
        """Start the client"""
        self.running = True
        self.pubsub_thread = self.pubsub.run_in_thread(sleep_time=0.001)
        await asyncio.sleep(2)
        await self.send_telecommand(b"TEST_COMMAND")
        await asyncio.sleep(1)
        await self.get_metrics("signal_strength")
        
    async def stop(self):
        """Stop the client"""
        self.running = False
        self.pubsub_thread.stop()

async def main():
    client = ClientComputer("modem1")
    try:
        await client.run()
        while client.running:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await client.stop()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    client = ClientComputer()
    asyncio.run(client.run())