import pytest
import os
import sys
import subprocess
import time
import aiohttp


@pytest.fixture(scope="session", autouse=True)
def start_stack():
    print("\n🚀 Starting stack with Docker Compose...")

    # Start Docker Compose
    subprocess.run(["docker-compose", "up", "-d"], check=True)

    # Wait for services to boot up (adjust as needed)
    time.sleep(5)

    yield  # Run tests here
    
    print("\n🧹 Stopping running Docker containers before teardown...")
    print("shell", sys.argv[0].lower())
    if os.name == "nt":  # For Windows
        subprocess.run('docker ps -q | foreach {docker stop $_}', shell=True, check=True)
    else:
        subprocess.run(["docker", "stop", "$(docker ps -q)"], shell=True, check=True)
    
    print("\n🧹 Waiting for containers to shut down...")
    time.sleep(2)

    subprocess.run(["docker-compose", "down", "--remove-orphans"], check=True)



@pytest.fixture(scope="module")
def base_url():
    return "http://localhost:8001"

@pytest.fixture(scope="module")
def tm_port():
    return 8002

@pytest.fixture(scope="module")
def tc_port():
    return 8003

@pytest.fixture(scope="module")
def aiohttp_timeout():
    return aiohttp.ClientTimeout(total=5)
