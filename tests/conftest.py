"""Shared test configuration and fixtures for the test suite."""

import pytest


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Provide sample data for tests.

    Returns:
        dict[str, str]: Dictionary containing sample test data
    """
    return {
        "app_name": "base-starter",
        "version": "0.1.0",
        "description": "Add your description here",
    }
