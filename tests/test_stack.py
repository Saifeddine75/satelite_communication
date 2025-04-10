import pytest
import asyncio
import aiohttp
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("ModemTester")

# ---------- Test API Endpoints ----------

@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", [
    "status",
    "signal_strength",
    "bit_error_rate",
    "statistics",
])
async def test_metrics_api(base_url, endpoint, aiohttp_timeout):
    url = f"{base_url}/metrics/{endpoint}"
    async with aiohttp.ClientSession(timeout=aiohttp_timeout) as session:
        async with session.get(url) as resp:
            assert resp.status == 200, f"{endpoint} failed with status {resp.status}"
            data = await resp.json()
            assert isinstance(data, dict), f"{endpoint} did not return a JSON object"
            logger.info(f"✅ {endpoint}: {data}")

# ---------- Test Telemetry Stream ----------

@pytest.mark.asyncio
async def test_telemetry_stream(tm_port):
    duration = 5  # seconds
    logger.info(f"🔄 Testing telemetry stream for {duration} seconds...")

    reader, writer = await asyncio.wait_for(
        asyncio.open_connection('localhost', tm_port), timeout=2
    )

    packet_count = 0
    start_time = datetime.now()

    try:
        while (datetime.now() - start_time).total_seconds() < duration:
            try:
                data = await asyncio.wait_for(reader.read(1024), timeout=1)
                if data:
                    packet_count += 1
            except asyncio.TimeoutError:
                continue
    finally:
        writer.close()
        await writer.wait_closed()

    assert packet_count > 0, "No telemetry packets received"
    logger.info(f"✅ Received {packet_count} telemetry packets in {duration} seconds")

# ---------- Test Telecommand ACK ----------

@pytest.mark.asyncio
@pytest.mark.parametrize("command", [
    b"PING",
    b"STATUS_REQ",
    b"CUSTOM_TC_123"
])
async def test_telecommand_ack(tc_port, command):
    reader, writer = await asyncio.wait_for(
        asyncio.open_connection('localhost', tc_port), timeout=2
    )

    writer.write(command)
    await writer.drain()

    ack = await asyncio.wait_for(reader.read(1024), timeout=2)

    writer.close()
    await writer.wait_closed()

    assert ack.startswith(b"ACK"), f"No valid ACK received for {command}"
    logger.info(f"✅ ACK received for command {command}: {ack.decode(errors='replace')}")
