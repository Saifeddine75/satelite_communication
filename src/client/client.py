# client_computer.py
import asyncio
import aiohttp
import logging

class ClientComputer:
    def __init__(self):
        self.logger = logging.getLogger("ClientComputer")
        self.running = False
        
    async def telemetry_listener(self):
        """Listen to TM stream"""
        while self.running:
            try:
                reader, writer = await asyncio.open_connection(
                    'localhost', 8001)
                self.logger.info("Connected to TM stream")
                
                while self.running:
                    data = await reader.read(1024)
                    if not data:
                        break
                    self.logger.info(f"Received TM: {data.hex()}")
                    
            except ConnectionError:
                self.logger.warning("TM Connection Error")
                await asyncio.sleep(1)
                
    async def send_telecommand(self, command):
        """Send a TC to modem"""
        try:
            reader, writer = await asyncio.open_connection(
                'localhost', 8002)
                
            writer.write(command)
            await writer.drain()
            
            # Wait for ACK
            ack = await reader.read(1024)
            if ack:
                self.logger.info(f"Received ACK: {ack.hex()}")
                
            writer.close()
            await writer.wait_closed()
            
        except ConnectionError as e:
            self.logger.error(f"Failed to send TC: {e}")
            
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
        """Run all client functions"""
        self.running = True
        await asyncio.gather(
            self.telemetry_listener(),
            self.monitor_metrics()
        )

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    client = ClientComputer()
    asyncio.run(client.run())