"""
conftest file.

This file is used to configure pytest.

Functions:
    - number_1(): Return a number.
    - number_2(): Return a number.
"""
import pytest


@pytest.fixture
def number_1():
    """Return a number."""
    return 10


@pytest.fixture
def number_2():
    """Return a number."""
    return 5
