"""Tests for RundeckConfig."""

from __future__ import annotations

import pytest

from rundeck_mcp.config import RundeckConfig


def test_defaults() -> None:
    cfg = RundeckConfig(_env_file=None)
    assert cfg.api_version == "41"
    assert cfg.verify_ssl is True
    assert cfg.timeout == 30.0


def test_api_base_strips_trailing_slash() -> None:
    cfg = RundeckConfig(base_url="https://rundeck.example.com/", api_token="t")
    assert cfg.api_base == "https://rundeck.example.com/api/41"


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RUNDECK_BASE_URL", "https://env.example.com")
    monkeypatch.setenv("RUNDECK_API_TOKEN", "env-token")
    monkeypatch.setenv("RUNDECK_API_VERSION", "42")
    monkeypatch.setenv("RUNDECK_VERIFY_SSL", "false")
    monkeypatch.setenv("RUNDECK_TIMEOUT", "12.5")

    cfg = RundeckConfig(_env_file=None)
    assert cfg.base_url == "https://env.example.com"
    assert cfg.api_token == "env-token"
    assert cfg.api_version == "42"
    assert cfg.verify_ssl is False
    assert cfg.timeout == 12.5
    assert cfg.api_base == "https://env.example.com/api/42"
