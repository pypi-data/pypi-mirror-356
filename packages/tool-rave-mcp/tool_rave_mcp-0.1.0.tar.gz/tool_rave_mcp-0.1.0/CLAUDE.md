# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tool Rave MCP is a universal MCP server proxy that enables parallel tool execution for MCP servers that don't support it natively. It acts as a middleware layer that intercepts MCP protocol messages and spawns fresh server processes for each tool call, allowing true parallelism.

## Core Architecture

The project has two main components:

1. **CLI Entry Point** (`src/toolrave/main.py`)
   - Typer-based CLI that accepts any MCP server command and arguments
   - Parses command-line arguments and passes them to the proxy
   - Handles graceful shutdown and error reporting

2. **MCP Proxy** (`src/toolrave/proxy.py`)
   - Core proxy logic that implements the MCP protocol interception
   - Maintains three key caches:
     - **Handshake cache**: Stores the initial MCP handshake sequence to replay for each worker
     - **Discovery cache**: Caches responses to `tools/list`, `prompts/list`, `resources/list` calls
     - **Worker pool**: Manages configurable number of concurrent worker threads
   - Each `tools/call` request spawns a fresh server process that replays the handshake and handles the call

## Key Architectural Patterns

- **Process Spawning**: For each tool call, spawns `subprocess.Popen(server_command)` with the original MCP server
- **Message Routing**: Different MCP methods are handled differently:
  - `initialize` → spawns server, caches handshake
  - `notifications/initialized` → added to handshake cache  
  - `tools/list`, `prompts/list`, `resources/list` → spawns server once, caches response
  - `tools/call` → queued for worker threads to handle in parallel
- **Environment Configuration**: All settings controlled via `TOOLRAVE_*` environment variables

## Common Development Commands

```bash
# Setup
just install                    # Install dependencies with uv

# Development workflow  
just check                      # Run all checks (lint, format, type-check)
just test                       # Run tests
just test-cov                   # Run tests with coverage report

# Individual checks
just lint                       # Run ruff linting with fixes
just format                     # Format code with ruff
just type-check                 # Run pyright type checking

# Testing the CLI
just run python server.py       # Test toolrave CLI with arguments
uv run toolrave --help          # Test CLI help

# Building
just build                      # Build package for distribution
```

## Testing Strategy

- **Unit tests** in `tests/` for both CLI and proxy components
- **CLI testing** uses `typer.testing.CliRunner` for command-line interface validation
- **Proxy testing** uses mocked subprocess calls to avoid spawning real servers
- **Coverage reporting** configured in pyproject.toml with pytest-cov

## Environment Variables

The proxy behavior is controlled entirely through environment variables:
- `TOOLRAVE_MAX_WORKERS` (default: 8) - Number of parallel worker threads
- `TOOLRAVE_ENABLE_LOGGING` (default: false) - Enable detailed request/response logging  
- `TOOLRAVE_LOG_DIR` (default: ~/.toolrave/logs) - Directory for log files

## Package Distribution

- Built with `hatchling` backend and distributed via `uv tool install`
- Entry point: `toolrave = "toolrave.main:app"` 
- Supports Python 3.9+ (configured in pyproject.toml)
- Dependencies: typer, rich (minimal runtime dependencies)