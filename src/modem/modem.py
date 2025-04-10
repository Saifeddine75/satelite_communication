import asyncio
from fastapi import FastAPI
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Modem")

class Modem:
    def __init__(self):
        self.app = FastAPI()
        self.telemetry_clients = set()
        self.telecommand_stats = {"received": 0, "last_tc": None}
        self.telemetry_stats = {"sent": 0}
        self._setup_api()
        self.test_packet = b"TEST_PACKET" * 10
        
    def _setup_api(self):
        @self.app.get("/metrics/status")
        async def get_status():
            return {"status": "healthy"}
            
        @self.app.get("/metrics/signal_strength")
        async def get_signal_strength():
            return {"signal_strength": 75}
            
        @self.app.get("/metrics/bit_error_rate")
        async def get_bit_error_rate():
            return {"bit_error_rate": 0.05}
            
        @self.app.get("/metrics/statistics")
        async def get_statistics():
            return {
                "telemetry_sent": self.telemetry_stats["sent"],
                "telecommands_received": self.telecommand_stats["received"],
                "last_telecommand": self.telecommand_stats["last_tc"]
            }
    
    async def handle_telemetry_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f"Telemetry client connected: {addr}")
        self.telemetry_clients.add(writer)
        
        try:
            while True:
                writer.write(self.test_packet)
                await writer.drain()
                self.telemetry_stats["sent"] += 1
                await asyncio.sleep(0.5)
        except ConnectionError:
            logger.info(f"Telemetry client disconnected: {addr}")
        finally:
            self.telemetry_clients.remove(writer)
            writer.close()
    
    async def handle_telecommand_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f"Telecommand client connected: {addr}")
        
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                    
                self.telecommand_stats["received"] += 1
                self.telecommand_stats["last_tc"] = data.hex()
                logger.info(f"Received TC: {data.hex()}")
                
                writer.write(b"ACK:" + data)
                await writer.drain()
        except ConnectionError:
            logger.info(f"Telecommand client disconnected: {addr}")
        finally:
            writer.close()
    
    async def run(self, host="0.0.0.0", ports=(8001, 8002, 8000)):
        """Start all services with ports (telemetry, telecommand, api)"""
        api_server = uvicorn.Server(
            config=uvicorn.Config(
                self.app,
                host=host,
                port=ports[2],
                log_level="info"
            )
        )
        
        servers = await asyncio.gather(
            asyncio.start_server(self.handle_telemetry_client, host, ports[0]),
            asyncio.start_server(self.handle_telecommand_client, host, ports[1]),
        )
        
        logger.info(f"Modem running:\n"
            f"- Telemetry: {host}:{ports[0]}\n"
            f"- Commands: {host}:{ports[1]}\n"
            f"- API: http://{host}:{ports[2]}")
        
        await asyncio.gather(
            api_server.serve(),
            *[s.serve_forever() for s in servers]
        )

if __name__ == "__main__":
    modem = Modem()
    try:
        asyncio.run(modem.run())  # Properly await the coroutine
    except KeyboardInterrupt:
        print("\nShutting down modem...")