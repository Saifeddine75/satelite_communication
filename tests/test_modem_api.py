import pytest
from fastapi import status
from src.modem.modem import Modem

@pytest.fixture(scope="module")
def modem_app():
    """Fixture to create the FastAPI app from the Modem"""
    modem = Modem()
    # modem.create_app()
    return modem.app

@pytest.mark.asyncio
def test_api_status(api_client):
    response = api_client.get("/metrics/status")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
def test_api_signal_strength(api_client):
    response = api_client.get("/metrics/signal_strength")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "signal_strength" in data
    assert isinstance(data["signal_strength"], int)

@pytest.mark.asyncio
def test_api_bit_error_rate(api_client):
    response = api_client.get("/metrics/bit_error_rate")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "bit_error_rate" in data
    assert 0 <= data["bit_error_rate"] <= 1

@pytest.mark.asyncio
def test_api_statistics(api_client):
    response = api_client.get("/metrics/statistics")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "telemetry_sent" in data
    assert "telecommands_received" in data
    assert "last_telecommand" in data