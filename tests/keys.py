"""Skip helpers for integration tests that need real API keys."""

import os

import pytest
from dotenv import dotenv_values


def _is_configured(name: str) -> bool:
    return bool(os.environ.get(name) or dotenv_values(".env").get(name))


def requires_keys(*names: str) -> pytest.MarkDecorator:
    """Skip the test unless every key is set in the environment or in .env."""
    missing = [name for name in names if not _is_configured(name)]
    return pytest.mark.skipif(bool(missing), reason=f"missing keys: {', '.join(missing)}")
