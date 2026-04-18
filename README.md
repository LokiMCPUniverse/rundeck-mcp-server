# Rundeck MCP Server

<div align="center">

# Rundeck Mcp Server

[![GitHub stars](https://img.shields.io/github/stars/LokiMCPUniverse/rundeck-mcp-server?style=social)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/LokiMCPUniverse/rundeck-mcp-server?style=social)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/network)
[![GitHub watchers](https://img.shields.io/github/watchers/LokiMCPUniverse/rundeck-mcp-server?style=social)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/watchers)

[![License](https://img.shields.io/github/license/LokiMCPUniverse/rundeck-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/LokiMCPUniverse/rundeck-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/LokiMCPUniverse/rundeck-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/LokiMCPUniverse/rundeck-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/commits)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-DC143C?style=for-the-badge)](https://modelcontextprotocol.io)

</div>

A Model Context Protocol (MCP) server for driving Rundeck from GenAI agents. Built on the
official `mcp` Python SDK (>=1.27) with FastMCP, an async `httpx` client, and
pydantic-settings for configuration.

## Features

- Project, job, execution and node tooling for Rundeck API v41+
- API-token authentication via the `X-Rundeck-Auth-Token` header
- Async httpx client with typed exceptions (`AuthenticationError`,
  `NotFoundError`, `APIError`)
- Managed client lifecycle via FastMCP `lifespan`
- Unit tests with mocked httpx (pytest-httpx)

## Installation

```bash
pip install rundeck-mcp-server
```

Or install from source:

```bash
git clone https://github.com/asklokesh/rundeck-mcp-server.git
cd rundeck-mcp-server
pip install -e .
```

## Configuration

Set the following environment variables (prefix `RUNDECK_`):

| Variable | Default | Description |
| --- | --- | --- |
| `RUNDECK_BASE_URL` | `http://localhost:4440` | Base URL of the Rundeck server |
| `RUNDECK_API_TOKEN` | *(empty)* | API token used for authentication |
| `RUNDECK_API_VERSION` | `41` | Rundeck API version |
| `RUNDECK_VERIFY_SSL` | `true` | Verify TLS certificates |
| `RUNDECK_TIMEOUT` | `30` | HTTP timeout (seconds) |

## Tools

- `list_projects`
- `list_jobs(project)`
- `get_job(job_id)`
- `run_job(job_id, options?, node_filter?)`
- `get_execution(execution_id)`
- `get_execution_output(execution_id)`
- `abort_execution(execution_id)`
- `list_executions(project, status?, max=20)`
- `list_nodes(project, filter?)`
- `enable_job_schedule(job_id)` / `disable_job_schedule(job_id)`
- `enable_job_execution(job_id)` / `disable_job_execution(job_id)`

## Running the server

```bash
rundeck-mcp
```

The server communicates over stdio per the MCP specification.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT License - see LICENSE file for details
