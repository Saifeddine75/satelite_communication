import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.client.client import ClientComputer

@pytest.mark.asyncio
async def test_telecommand_published_to_redis():
    """Verify that send_telecommand publishes a message to Redis"""

    with patch("src.client.client.redis.Redis") as mock_redis_class:
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.publish = Mock()

        client = ClientComputer("test_modem")  # Assuming it uses redis.Redis inside

        await client.send_telecommand(b"test")

        mock_redis_instance.publish.assert_called_once_with(
            "modem:test_modem:telecommand",
            b"test".hex()
        )