from __future__ import annotations

from collections.abc import Generator

import pytest
import structlog
from pytest_mock import MockFixture


@pytest.fixture(autouse=True)
def reset_config() -> Generator[None, None, None]:
    structlog.reset_defaults()
    yield
    structlog.reset_defaults()


@pytest.fixture(autouse=True)
def mock_journald_connected(mocker: MockFixture) -> Generator[None, None, None]:
    """Mock is_journald_connected to always return True."""
    mocker.patch(
        'structlog_journald.processors.is_journald_connected',
        return_value=True,
    )
    yield
