import pytest
import asyncio
import aiohttp
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Tester")

@pytest.mark.asyncio
class StackTester:
    def __init__(self):
        self.base_api_url = "http://localhost:8000"
        self.tm_port = 8001  
        self.tc_port = 8002
        self.timeout = aiohttp.ClientTimeout()

    async def test_metrics_api(self):
        """Test all modem metrics endpoints"""
        endpoints = [
            'status',
            'signal_strength',
            'bit_error_rate',
            'statistics'
        ]
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            for endpoint in endpoints:
                try:
                    url = f"{self.base_api_url}/metrics/{endpoint}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        logger.info(f"Metric {endpoint}: {data}")
                except Exception as e:
                    logger.error(f"Failed to test {endpoint}: {str(e)}")

    async def test_telemetry_stream(self, duration=5):
        """Test TM downlink stream during a specified duration"""
        logger.info(f"Testing TM stream for {duration} seconds...")
        start_time = datetime.now()
        
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection('localhost', self.tm_port),
                timeout=2
            )
            
            packet_count = 0
            while (datetime.now() - start_time).total_seconds() < duration:
                try:
                    data = await asyncio.wait_for(reader.read(1024), timeout=1)
                    if not data:
                        break
                    packet_count += 1
                    logger.debug(f"Received TM packet {packet_count}: {data[:16].hex()}...")
                except asyncio.TimeoutError:
                    continue
            
            writer.close()
            await writer.wait_closed()
            logger.info(f"Received {packet_count} TM packets in {duration} seconds")
            
        except Exception as e:
            logger.error(f"TM test failed: {str(e)}")

    async def test_telecommand(self, command=b"TEST_TC"):
        """Test TC uplink with acknowledgment"""
        logger.info(f"Sending TC: {command.decode(errors='replace')}")
        
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection('localhost', self.tc_port),
                timeout=2
            )
            
            writer.write(command)
            await writer.drain()
            
            ack = await asyncio.wait_for(reader.read(1024), timeout=2)
            if ack.startswith(b"ACK"):
                logger.info(f"Received ACK: {ack.decode(errors='replace')}")
            else:
                logger.warning(f"Unexpected response: {ack.hex()}")
            
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            logger.error(f"TC test failed: {str(e)}")

    async def run_tests(self):
        """Run all tests sequentially"""
        logger.info("Starting Modem API tests...")
        await self.test_metrics_api()
        
        logger.info("\nStarting Telemetry stream test...")
        await self.test_telemetry_stream()
        
        logger.info("\nStarting Telecommand tests...")
        test_commands = [
            b"PING",
            b"STATUS_REQ",
            b"CUSTOM_TC_123"
        ]
        for cmd in test_commands:
            await self.test_telecommand(cmd)
            await asyncio.sleep(1)  # Brief pause between commands

@pytest.mark.asyncio
async def main():
    tester = StackTester()
    await tester.run_tests()

if __name__ == "__main__":
    # Windows-specific event loop policy
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Testing interrupted by user")
    except Exception as e:
        logger.error(f"Critical error during testing: {str(e)}")