import asyncio
import logging
import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ClientComputer")

class ClientComputer:
    def __init__(self, modem_id: str, redis_host:str ="localhost"):
        self.modem_id = modem_id
        self.redis = redis.Redis(host=redis_host)
        self.pubsub = self.redis.pubsub()
        
    async def send_telecommand(self, data: bytes):
        """Send telecommand to modem with Redis"""
        self.redis.publish(f"modem:{self.modem_id}:telecommand", data.hex())
        logger.info(f"Sent telecommand: {data.hex()}")
            
    async def run(self):
        """Start the client"""
        self.pubsub_thread = self.pubsub.run_in_thread()
        await self.send_telecommand(b"TEST_COMMAND")

    async def stop(self):
        """Stop the client"""
        self.pubsub_thread.stop()

async def main():
    client = ClientComputer("modem")
    try:
        await client.run()
    except KeyboardInterrupt:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())