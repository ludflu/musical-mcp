# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses `uv` as the Python package manager and includes a Makefile for common tasks:

### Makefile Commands (Recommended)
- **Install dependencies**: `make install`
- **Run the application**: `make run`
- **Run tests**: `make test`
- **Run tests with coverage**: `make test-cov`
- **Format code**: `make format`
- **Type checking**: `make type-check`
- **Run all linting**: `make lint`
- **Clean cache files**: `make clean`
- **Build Docker image**: `make docker-build`
- **Run Docker container**: `make docker-run`
- **Full development workflow**: `make all`
- **CI workflow**: `make ci`

### Direct uv Commands
- **Run the application**: `uv run src/main.py`
- **Run tests**: `uv run pytest`
- **Run tests with coverage**: `uv run pytest --cov`
- **Format code**: `uv run black .`
- **Sort imports**: `uv run isort .`
- **Type checking**: `uv run pyright`
- **Install dependencies**: `uv sync`
- **Add new dependency**: `uv add <package_name>`
- **Add dev dependency**: `uv add --dev <package_name>`

## Project Structure

The project is configured with standard Python development tools:
- Black for code formatting
- isort for import sorting  
- Pyright for type checking
- Pytest for testing (with coverage and mock plugins)

## Development Setup

The project requires Python 3.12+ and uses uv for dependency management. Run `uv sync` to set up the development environment.

## Coding Guidelines

- write unit tests for new code
- run the tests to make sure everything works
- keep functions small - 20 lines max
- add doc strings for all functions including the arguments and return values
- include types for all function arguments and return values
- keep test coverage above 75 %
- make sure the docker image builds
- use the Makefile targets to run all project actions
