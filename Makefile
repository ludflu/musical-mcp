.PHONY: help install test test-cov lint format type-check clean run docker-build docker-run all

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  run         - Run the application"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run all linting (format + type-check)"
	@echo "  format      - Format code with black and isort"
	@echo "  type-check  - Run type checking with pyright"
	@echo "  clean       - Clean up cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run Docker container"
	@echo "  all         - Run install, lint, and test"

# Install dependencies
install:
	uv sync

# Run the application
run:
	uv run python src/main.py C Major cmajor.mid
	uv run python src/main.py C dorian dorian.mid
	uv run python src/main.py C pentatonicMajor -o 3 pentatonicMajor.mid
	uv run python src/main.py C pentatonicMinor -o 3 pentatonicMinor.mid

# Run tests
test:
	uv run pytest -v

# Run tests with coverage
test-cov:
	uv run pytest --cov --cov-report=html --cov-report=term

# Format code
format:
	uv run isort .
	uv run black .

# Type checking
type-check:
	uv run pyright

# Run all linting
lint: format type-check

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

# Docker targets
docker-build:
	docker build -t musical-mcp .

docker-run:
	docker run --rm musical-mcp

# Run full development workflow
all: install lint test

# Continuous integration target
ci: install lint test-cov
