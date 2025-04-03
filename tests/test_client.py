import pytest
from unittest.mock import Mock, patch
from client.client import ClientComputer

@pytest.mark.asyncio
async def test_telecommand_published_to_redis():
    """Verify client publishes telecommands to Redis"""
    with patch('redis.Redis') as mock_redis:
        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.pubsub.return_value = Mock()
        
        client = ClientComputer("test_modem")
        await client.send_telecommand(b"test")
        
        mock_redis_instance.publish.assert_called_with(
            "modem:test_modem:telecommand",
            b"test".hex()
        )