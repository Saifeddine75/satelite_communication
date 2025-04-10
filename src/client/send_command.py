import asyncio

async def send_telecommand(command: bytes):
    reader, writer = await asyncio.open_connection('localhost', 8002)
    writer.write(command)
    await writer.drain()
    response = await reader.read(100)
    print(f"Received ACK: {response.decode()}")
    writer.close()

asyncio.run(send_telecommand(b"TEST"))