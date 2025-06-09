# Rundeck MCP Server

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
