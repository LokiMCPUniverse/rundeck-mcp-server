"""Configuration for the Rundeck MCP server."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RundeckConfig(BaseSettings):
    """Runtime configuration loaded from environment variables.

    All settings are prefixed with ``RUNDECK_`` (e.g. ``RUNDECK_BASE_URL``).
    """

    model_config = SettingsConfigDict(
        env_prefix="RUNDECK_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    base_url: str = Field(
        default="http://localhost:4440",
        description="Base URL for the Rundeck server (no trailing slash).",
    )
    api_token: str = Field(
        default="",
        description="Rundeck API token used in the X-Rundeck-Auth-Token header.",
    )
    api_version: str = Field(
        default="41",
        description="Rundeck API version to target.",
    )
    verify_ssl: bool = Field(
        default=True,
        description="Verify TLS certificates when talking to Rundeck.",
    )
    timeout: float = Field(
        default=30.0,
        description="HTTP request timeout in seconds.",
    )

    @property
    def api_base(self) -> str:
        """Return the full API base URL including version, no trailing slash."""
        return f"{self.base_url.rstrip('/')}/api/{self.api_version}"
