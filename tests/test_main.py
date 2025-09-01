"""Tests for the main module."""

from io import StringIO
from unittest.mock import patch

import pytest

from src.main import main


class TestMain:
    """Test cases for main functionality."""

    def test_main_prints_hello_message(self) -> None:
        """Test that main() prints the expected hello message.

        Verifies that the main function outputs the correct greeting
        to stdout when called.
        """
        with patch("sys.stdout", new=StringIO()) as fake_out:
            main()
            assert fake_out.getvalue().strip() == "Hello from base-starter!"

    def test_main_function_exists(self) -> None:
        """Test that main function is callable.

        Basic smoke test to ensure the main function can be imported
        and is callable without raising exceptions.
        """
        assert callable(main)
        # Should not raise any exceptions
        main()
