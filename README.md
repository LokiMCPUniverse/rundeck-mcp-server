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

[![Commit Activity](https://img.shields.io/github/commit-activity/m/LokiMCPUniverse/rundeck-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/pulse)
[![Code Size](https://img.shields.io/github/languages/code-size/LokiMCPUniverse/rundeck-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/rundeck-mcp-server)
[![Contributors](https://img.shields.io/github/contributors/LokiMCPUniverse/rundeck-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/rundeck-mcp-server/graphs/contributors)

</div>

A Model Context Protocol (MCP) server for integrating Rundeck with GenAI applications.

## Overview

Runbook automation and job scheduling

## Features

- Comprehensive Rundeck API coverage
- Multiple authentication methods
- Enterprise-ready with rate limiting
- Full error handling and retry logic
- Async support for better performance

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

Create a `.env` file or set environment variables according to Rundeck API requirements.

## Quick Start

```python
from rundeck_mcp import RundeckMCPServer

# Initialize the server
server = RundeckMCPServer()

# Start the server
server.start()
```

## License

MIT License - see LICENSE file for details
