"""Shared pytest fixtures for Rundeck MCP tests."""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
import pytest_asyncio

from rundeck_mcp.client import RundeckClient
from rundeck_mcp.config import RundeckConfig


@pytest.fixture
def config() -> RundeckConfig:
    return RundeckConfig(
        base_url="http://rundeck.test:4440",
        api_token="test-token",
        api_version="41",
        verify_ssl=False,
        timeout=5.0,
    )


@pytest_asyncio.fixture
async def client(config: RundeckConfig) -> AsyncIterator[RundeckClient]:
    c = RundeckClient(config)
    try:
        yield c
    finally:
        await c.aclose()


@pytest.fixture
def api_base(config: RundeckConfig) -> str:
    return config.api_base
