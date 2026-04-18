"""Tests for the FastMCP server wiring."""

from __future__ import annotations

from rundeck_mcp import server as server_module
from rundeck_mcp.server import mcp


async def test_tools_are_registered() -> None:
    tools = await mcp.list_tools()
    names = {tool.name for tool in tools}

    expected = {
        "list_projects",
        "list_jobs",
        "get_job",
        "run_job",
        "get_execution",
        "get_execution_output",
        "abort_execution",
        "list_executions",
        "list_nodes",
        "enable_job_schedule",
        "disable_job_schedule",
        "enable_job_execution",
        "disable_job_execution",
    }
    missing = expected - names
    assert not missing, f"missing tools: {missing}"


def test_main_exists() -> None:
    assert callable(server_module.main)
