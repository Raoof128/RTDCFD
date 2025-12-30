.PHONY: help install install-dev test lint format security clean build docs run dashboard validate

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run all tests"
	@echo "  test-unit    - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  lint         - Run code linting"
	@echo "  format       - Format code"
	@echo "  security     - Run security checks"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build distribution packages"
	@echo "  docs         - Build documentation"
	@echo "  run          - Run simulation"
	@echo "  dashboard    - Start dashboard"
	@echo "  validate     - Validate configuration"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e .[dev]
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-unit:
	pytest tests/test_scenarios.py tests/test_basic_functionality.py -v

test-integration:
	pytest tests/test_config.py -v

test-coverage:
	pytest --cov=agents --cov=orchestration --cov=utils --cov=scenarios --cov=dashboard --cov=mcp_servers --cov-report=html --cov-report=term-missing

test-parallel:
	pytest -n auto tests/

# Code Quality
lint:
	flake8 agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ --max-line-length=88 --extend-ignore=E203,W503,E501
	mypy agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/ --ignore-missing-imports
	bandit -r agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/

format:
	black agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/
	isort agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/

format-check:
	black --check agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/
	isort --check-only agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/

# Security
security:
	bandit -r agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/
	safety check
	pip-audit

security-full:
	bandit -r agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/
	safety check
	pip-audit
	semgrep --config=.semgrep.yml agents/ orchestration/ utils/ scenarios/ dashboard/ mcp_servers/

# Quality Assurance
quality: lint format-check security test

quality-all: format lint security test-coverage

# Development
dev-setup: install-dev
	@echo "Development environment setup complete"

dev-test: test-unit test-integration
	@echo "Development tests complete"

dev-lint: lint
	@echo "Development linting complete"

dev-format: format
	@echo "Development formatting complete"

dev-security: security
	@echo "Development security checks complete"

# Build and Distribution
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf docs/_build/

build: clean
	python -m build
	twine check dist/*

# Documentation
docs:
	sphinx-build -b html docs/ docs/_build/html

docs-serve:
	cd docs/_build/html && python -m http.server 8000

docs-clean:
	rm -rf docs/_build/

# Application
validate:
	python main.py --validate-config

run:
	python main.py --scenario soci_energy_grid

run-telco:
	python main.py --scenario soci_telco_network

run-water:
	python main.py --scenario soci_water_system

run-headless:
	python main.py --scenario soci_energy_grid --headless

dashboard:
	streamlit run dashboard/streamlit_ui.py

dashboard-dev:
	STREAMLIT_SERVER_PORT=8501 streamlit run dashboard/streamlit_ui.py

# Scenarios
scenarios:
	python -c "import scenarios; print(scenarios.get_available_scenarios())"

validate-scenarios:
	python -c "import scenarios; scenarios.validate_all_scenarios()"

# System Health
health:
	python -c "from utils.validation_standalone import check_system_health; check_system_health()"

# Performance
perf:
	pytest --benchmark-only tests/

profile:
	pytest --profile tests/ --profile-svg

# CI/CD
ci: quality-all build
	@echo "CI pipeline complete"

# Docker (if needed)
docker-build:
	docker build -t autonomous-multi-agent-simulation .

docker-run:
	docker run -p 8501:8501 autonomous-multi-agent-simulation

# Release
release: clean test-coverage build
	@echo "Release ready"

# Development shortcuts
dev: install-dev format lint test
	@echo "Development cycle complete"

quick-test: test-unit
	@echo "Quick tests complete"

full-test: test-coverage
	@echo "Full tests complete"

# Maintenance
update-deps:
	pip install --upgrade -r requirements.txt
	pip install --upgrade -r requirements-dev.txt

check-deps:
	pip-audit --requirement requirements.txt
	safety check

# Utilities
count:
	@echo "Python files:"
	@find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | wc -l
	@echo "Lines of code:"
	@find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -exec wc -l {} + | awk '{sum += $$1} END {print sum}'

size:
	du -sh --exclude=".git" --exclude="venv" --exclude=".venv" --exclude="__pycache__" .

info:
	@echo "Project: Autonomous Multi-Agent Red/Blue Team Simulation System"
	@echo "Python: $(shell python --version)"
	@echo "Pip: $(shell pip --version)"
	@echo "Virtual Environment: $(shell python -c 'import sys; print(sys.prefix)' | sed 's/None/None/')"

# Environment variables
env:
	@echo "Required environment variables:"
	@echo "  ANTHROPIC_API_KEY - Anthropic API key for Claude 3.5 Sonnet"
	@echo "Optional environment variables:"
	@echo "  LOG_LEVEL - Logging level (DEBUG, INFO, WARNING, ERROR)"
	@echo "  ENABLE_CONSOLE_OUTPUT - Enable console logging (true/false)"
	@echo "  SIMULATION_MODE_ONLY - Ensure simulation-only mode (true/false)"

# Setup for new contributors
setup: install-dev
	@echo "Setup complete! You can now:"
	@echo "  - Run 'make test' to run tests"
	@echo "  - Run 'make lint' to check code quality"
	@echo "  - Run 'make format' to format code"
	@echo "  - Run 'make security' to check security"
	@echo "  - Run 'make run' to run the simulation"
	@echo "  - Run 'make dashboard' to start the dashboard"

# Quick start for development
start: install-dev
	@echo "Starting development environment..."
	@echo "Running validation..."
	python main.py --validate-config
	@echo "Running tests..."
	make test-unit
	@echo "Starting dashboard..."
	make dashboard

# Production deployment check
prod-check: security test-coverage
	@echo "Production deployment checks complete"
