.PHONY: help install venv migrate test lint format clean run docker-build docker-up docker-down requirements install-dev install-prod requirements compile-deps sync-deps-dev sync-deps-prod

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/Scripts/python
PIP = $(VENV_DIR)/Scripts/pip
PIP_COMPILE = $(VENV_DIR)/Scripts/pip-compile
PIP_SYNC = $(VENV_DIR)/Scripts/pip-sync
MANAGE = $(PYTHON) manage.py

help:
	@echo "Available commands:"
	@echo "install    - Install dependencies"
	@echo "venv      - Create virtual environment"
	@echo "migrate   - Apply migrations"
	@echo "test      - Run tests"
	@echo "lint      - Check code"
	@echo "format    - Format code"
	@echo "clean     - Clean project"
	@echo "run       - Run development server"
	@echo "docker-build - Build Docker images"
	@echo "docker-up    - Start Docker containers"
	@echo "docker-down  - Stop Docker containers"
	@echo "install-dev  - Install development dependencies"
	@echo "install-prod - Install production dependencies"
	@echo "requirements - Update requirements files"
	@echo "compile-deps - Compile dependencies"
	@echo "sync-deps-dev - Sync dev dependencies"
	@echo "sync-deps-prod - Sync prod dependencies"

# Create virtual environment
venv:
	python -m venv $(VENV_DIR)
	@echo "=== Virtual environment created ==="
	@echo "Virtual environment created. Activate it with the command: source $(VENV_DIR)/Scrip/activate"

# Activate virtual environment
activate:
	@echo "To activate the virtual environment, run in the terminal:"
	@echo "source $(VENV_DIR)/Scripts/activate"

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	@echo "=== Migrations applied ==="

test:
	$(PYTHON) -m pytest
	@echo "=== Tests completed ==="

lint:
	$(VENV_DIR)/Scrip/flake8 apps/ config/
	@echo "=== Code check completed ==="

format:
	$(VENV_DIR)/Scrip/black apps/ config/
	@echo "=== Code formatted ==="

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "=== Project cleaned ==="

run:
	$(MANAGE) runserver
	@echo "=== Server started ==="

docker-build:
	docker-compose build
	@echo "=== Docker images built ==="

docker-up:
	docker-compose up -d
	@echo "=== Docker containers started ==="

docker-down:
	docker-compose down
	@echo "=== Docker containers stopped ==="

# Install all development dependencies
install-dev:
	$(PIP) install -r requirements/dev.txt

# Install production dependencies
install-prod:
	$(PIP) install -r requirements/prod.txt

# Update dependency files
requirements:
	$(PIP) freeze > requirements/base.txt
	$(PIP) freeze > requirements/dev.txt
	$(PIP) freeze > requirements/prod.txt


compile-deps:
	@echo "Compiling dependencies..."
	$(PIP_COMPILE) requirements/base.in
	$(PIP_COMPILE) requirements/dev.in
	$(PIP_COMPILE) requirements/prod.in
	@echo "=== Dependencies compiled ==="

sync-deps-dev:
	@echo "Syncing dev dependencies..."
	$(PIP_SYNC) requirements/dev.txt
	@echo "=== Dev dependencies synced ==="

sync-deps-prod:
	@echo "Syncing prod dependencies..."
	$(PIP_SYNC) requirements/prod.txt
	@echo "=== Prod dependencies synced ===" 