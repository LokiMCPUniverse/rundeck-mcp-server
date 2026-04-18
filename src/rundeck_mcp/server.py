"""FastMCP server exposing Rundeck operations as MCP tools."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

from .client import RundeckClient
from .config import RundeckConfig


@dataclass
class AppContext:
    """Runtime context shared with tool handlers via ``ctx.request_context``."""

    client: RundeckClient
    config: RundeckConfig


@asynccontextmanager
async def lifespan(_server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage the lifecycle of the Rundeck HTTP client."""
    config = RundeckConfig()
    client = RundeckClient(config)
    try:
        yield AppContext(client=client, config=config)
    finally:
        await client.aclose()


mcp = FastMCP("rundeck-mcp-server", lifespan=lifespan)


def _client(ctx: Context) -> RundeckClient:
    app_ctx: AppContext = ctx.request_context.lifespan_context
    return app_ctx.client


@mcp.tool()
async def list_projects(ctx: Context) -> Any:
    """List all Rundeck projects visible to the configured API token."""
    return await _client(ctx).list_projects()


@mcp.tool()
async def list_jobs(project: str, ctx: Context) -> Any:
    """List jobs defined in the given Rundeck project."""
    return await _client(ctx).list_jobs(project)


@mcp.tool()
async def get_job(job_id: str, ctx: Context) -> Any:
    """Return the full definition for a single Rundeck job."""
    return await _client(ctx).get_job(job_id)


@mcp.tool()
async def run_job(
    job_id: str,
    ctx: Context,
    options: dict[str, Any] | None = None,
    node_filter: str | None = None,
) -> Any:
    """Execute a Rundeck job with optional options and node filter."""
    return await _client(ctx).run_job(job_id, options=options, node_filter=node_filter)


@mcp.tool()
async def get_execution(execution_id: str, ctx: Context) -> Any:
    """Retrieve metadata for a specific Rundeck execution."""
    return await _client(ctx).get_execution(execution_id)


@mcp.tool()
async def get_execution_output(execution_id: str, ctx: Context) -> Any:
    """Fetch the log output for a Rundeck execution."""
    return await _client(ctx).get_execution_output(execution_id)


@mcp.tool()
async def abort_execution(execution_id: str, ctx: Context) -> Any:
    """Abort a running Rundeck execution (uses GET per Rundeck spec)."""
    return await _client(ctx).abort_execution(execution_id)


@mcp.tool()
async def list_executions(
    project: str,
    ctx: Context,
    status: str | None = None,
    max: int = 20,
) -> Any:
    """List recent executions for a project, optionally filtered by status."""
    return await _client(ctx).list_executions(project, status=status, max_results=max)


@mcp.tool()
async def list_nodes(
    project: str,
    ctx: Context,
    filter: str | None = None,
) -> Any:
    """List nodes registered to a project, optionally applying a node filter."""
    return await _client(ctx).list_nodes(project, filter=filter)


@mcp.tool()
async def enable_job_schedule(job_id: str, ctx: Context) -> Any:
    """Enable the cron schedule for a job."""
    return await _client(ctx).enable_job_schedule(job_id)


@mcp.tool()
async def disable_job_schedule(job_id: str, ctx: Context) -> Any:
    """Disable the cron schedule for a job."""
    return await _client(ctx).disable_job_schedule(job_id)


@mcp.tool()
async def enable_job_execution(job_id: str, ctx: Context) -> Any:
    """Allow the job to be executed (on-demand or scheduled)."""
    return await _client(ctx).enable_job_execution(job_id)


@mcp.tool()
async def disable_job_execution(job_id: str, ctx: Context) -> Any:
    """Prevent the job from being executed."""
    return await _client(ctx).disable_job_execution(job_id)


def main() -> None:
    """Entry point for the ``rundeck-mcp`` script."""
    mcp.run()


if __name__ == "__main__":
    main()
