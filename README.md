## Introduction

A Python-based simulation of ground station communication with satellite systems, handling telemetry, telecommands, and modem metrics.

## System Architecture

![alt text](image.png)

### Modem

Modules:

- **Telemetry Server**: Send telemetries using TCP socket port 8000
- **Telecommands Server**: Receive telecommands using TCP socket port 8001

- **Modem API Endpoints**:
  - `GET /metrics/status`
  - `GET /metrics/signal_strength`
  - `GET /metrics/bit_error_rate`
  - `GET /metrics/statistics`

### Client with Redis

Modules:

- **Telemetry Server**: Receive telemetries using port 8001 (implement redis connection for efficiency)
- **Telecommands Server**: Send telecommands using port 8002 (implement redis connection for efficiency)

### Deployment

Deploy client and modem services

`docker-compose up --build`

### Test/Validation

Deploy your app and execute this script:

`python scripts/test_stack.py`
