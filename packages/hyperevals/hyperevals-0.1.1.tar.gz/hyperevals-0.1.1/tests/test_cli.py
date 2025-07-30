"""
Tests for the CLI module.
"""

import pytest

from hyperevals import __version__
from hyperevals.cli import create_parser, main


def test_version_flag():
    """Test that --version flag works correctly."""
    result = main(["--version"])
    assert result == 0


def test_create_parser():
    """Test that the argument parser is created correctly."""
    parser = create_parser()
    assert parser.prog == "hyperevals"

    # Test parsing version flag
    args = parser.parse_args(["--version"])
    assert args.version is True

    # Test parsing config file
    args = parser.parse_args(["config.yaml"])
    assert args.config == "config.yaml"


def test_main_without_args():
    """Test main function without arguments."""
    result = main([])
    assert result == 0


def test_main_with_config():
    """Test main function with config file."""
    result = main(["config.yaml"])
    assert result == 0
