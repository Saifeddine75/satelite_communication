include var/os_variables.mk

# ----------------------------------
# App settings
# ----------------------------------
FAST_APP_MODULE=src.main:create_app
HOST=0.0.0.0
PORT=8000
APP_DIR=src
APP_TEST_DIR=tests
IMAGE_NAME=satellite-communication
TAG=latest

# ----------------------------------
# Default Help
# ----------------------------------
.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo "Available targets:"
	@echo "  venv         - Create virtual environment"
	@echo "  install      - Install Python dependencies"
	@echo "  run          - Run FastAPI app with Uvicorn"
	@echo "  test         - Run tests with pytest"
	@echo "  lint         - Lint code using ruff"
	@echo "  format       - Format code using black"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"
	@echo "  docker-push  - Push Docker image to registry"
	@echo "  clean        - Remove venv and __pycache__"

# ----------------------------------
# Python Environment & Install
# ----------------------------------

.PHONY: venv
venv:	
	uv venv $(VENV)

.PHONY: install
install: venv
	uv sync
	uv lock

.PHONY: install-dev
install-dev: venv
	uv sync --group dev
	uv lock


# ----------------------------------
# App Run
# ----------------------------------
.PHONY: run
run:
	python $(APP_DIR)\main.py

run2:
	uvicorn $(FAST_APP_MODULE) --host $(HOST) --port $(PORT) --no-reload


# ----------------------------------
# Formatting, Linting
# ----------------------------------
.PHONY: check-black
check-black:
	black $(APP_DIR) $(APP_TEST_DIR)

.PHONY: check-lint
check-lint:
	ruff check $(APP_DIR) $(APP_TEST_DIR)

.PHONY: check-bandit
check-bandit:
	bandit -r $(APP_DIR) $(APP_TEST_DIR)

.PHONY: check-isort
check-isort:
	isort $(APP_DIR) $(APP_TEST_DIR)

.PHONY: check-typing
check-typing:
	mypy $(APP_DIR) $(APP_TEST_DIR)


.PHONY: check-all
check-all: check-black check-lint check-isort check-typing
	check-black
	check-lint
	check-isort
	check-typing
	check-bandit
	echo "Quality checks passed!"

fix-lint:
	ruff check $(APP_DIR) $(APP_TEST_DIR) --fix 

# ----------------------------------
# Test & Validation
# ----------------------------------

.PHONY: test
test:
	pytest $(APP_DIR) $(APP_TEST_DIR)


.PHONY: validate-stack
validate-stack:
	docker compose up --build -d
	python scripts/validate_stack.py

# ----------------------------------
# Docker
# ----------------------------------
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

.PHONY: docker-run
docker-run:
	docker run -p 8000:8000 $(IMAGE_NAME):$(TAG)

.PHONY: docker-push
docker-push:
	docker push $(IMAGE_NAME):$(TAG)


# ----------------------------------
# Clean cache
# ----------------------------------
.PHONY: clean
clean:
	-@$(DEL_CMD) *.pyc 2> nul
	-@$(DEL_CMD) .\*.pyo 2> nul
	-@$(DEL_CMD) .\*.pyd 2> nul
	-@$(DEL_CMD) .\pytest_cache\* 2> nul
	-$(CLEAN_CACHE)


# ----------------------------------
# Clean
# ----------------------------------
.PHONY: clean-venv
clean-venv:
	$(RMDIR_CMD) .venv