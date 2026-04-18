"""Typed exception hierarchy for the Rundeck MCP server."""

from __future__ import annotations


class RundeckError(Exception):
    """Base class for all Rundeck MCP server errors."""


class AuthenticationError(RundeckError):
    """Raised when Rundeck rejects our API token (HTTP 401/403)."""


class NotFoundError(RundeckError):
    """Raised when a Rundeck resource cannot be found (HTTP 404)."""


class APIError(RundeckError):
    """Raised for other non-successful Rundeck API responses."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
