"""
Pytest configuration for C-Xool test suite.
Handles warnings.
"""

import warnings


def pytest_configure():
    """Configure pytest to avoid 'size changed' warnings."""
    warnings.filterwarnings("ignore", message="numpy.ndarray size changed")
