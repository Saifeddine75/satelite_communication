# Satellite Communication Stack

A Python-based simulation of ground station communication with satellite systems, handling telemetry, telecommands, and modem metrics.

## Table of Contents

- [System Architecture](#system-architecture)
- [Setup Dev Environment](#setup-dev-environment)
- [Testing & Validation](#testing--validation)

## 🧠 System Architecture

![alt text](image.png)

### 🛰️ Modem

Modules:

- **Telemetry Server**: Send telemetries using TCP socket port 8000
- **Telecommands Server**: Receive telecommands using TCP socket port 8001

- **Modem API Endpoints**:
  - `GET /metrics/status`
  - `GET /metrics/signal_strength`
  - `GET /metrics/bit_error_rate`
  - `GET /metrics/statistics`

### 🖥️ Simple ClientComputer

Modules:

- **Telemetry Server**: Receive telemetries using port 8001 (implement redis connection for efficiency)
- **Telecommands Server**: Send telecommands using port 8002 (implement redis connection for efficiency)

### 🖥️ ClientComputer with Redis

Redis is known for its high performance and low-latency. It ensures fast asynchronous data transmission using a pub/sub protocol.

Modules:

- **Telemetry Server**: Receive telemetries after subscribing to Redis topic. The client server listens for incoming telemetry messages published by the modem.
- **Telecommands Server**: Send telecommands to the modem through Redis. The client server publishes commands to redis that are readed by the modem that have subscribed to this redis channel.

## ⚙️ Configure your environment

First, install python-uv package, this package allows to manage python the project and dependencies efficiently.
Furthermore, like poetry it ensuring running reproductibility using a lock file.

### 1. Install `python-uv` Package Manager

`pip install python-uv`

### 2. Create your virtual env vile and activate it:

`uv venv .venv`
`source .venv/bin/activate   # On Windows: .venv\Scripts\activate`

### 3. Install and lock the packages with uv using pyproject.toml file:

`uv sync`
or
`uv sync --extra test` for test environment
`uv lock`

## 🚀 Deployment

Deploy client and modem services

`docker-compose up --build`

## ✅ Test/Validation

Deploy your app and execute this script to test the stack:
`python scripts/validate_stack.py`

This script verifies:

- Telecommands transmission from client ➝ modem
- Telemetry transmission from modem ➝ client

## Roadmap

- [x] Setup the dev environment
- [x] Develop ClientComputer module
- [x] Develop Modem module
- [x] Deploy your stack
- [x] Test & Validate the POC
- [ ] Monitor and optimization and performances (Redis)
