# Tool Rave MCP

Universal MCP server proxy that enables parallel tool execution for servers that don't support it natively.

<div align="center">
  <img src=".github/simple_meme.png" alt="Tool Rave MCP solves the parallel execution problem" width="400">
</div>

## What it does

Many MCP servers handle tool calls sequentially, which can be slow when you need to run multiple tools in parallel. Tool Rave acts as a proxy that:

1. **Caches handshakes** - Stores the initial handshake sequence to replay for each tool call
2. **Caches discovery** - Stores responses to `tools/list`, `prompts/list`, and `resources/list` calls
3. **Spawns parallel workers** - Creates fresh server processes for each `tools/call` request
4. **Manages worker pool** - Configurable number of concurrent workers (default: 8)

## Installation

Install using `uv`:

```bash
uv tool install tool-rave-mcp
```

Or install from source:

```bash
git clone <repo-url>
cd tool-rave-mcp
uv sync
uv run toolrave --help
```

## Usage

Instead of running your MCP server directly:

```bash
# Before
python your_mcp_server.py

# After
toolrave python your_mcp_server.py
```

Works with any command and arguments:

```bash
toolrave python server.py --config config.json --verbose
toolrave uv run --script mcp_server.py
toolrave ./my_server --port 8080
```

## Configuration

Configure via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `TOOLRAVE_MAX_WORKERS` | `8` | Maximum number of parallel workers |
| `TOOLRAVE_ENABLE_LOGGING` | `false` | Enable detailed logging |
| `TOOLRAVE_LOG_DIR` | `~/.toolrave/logs` | Directory for log files |

Example:

```bash
export TOOLRAVE_MAX_WORKERS=16
export TOOLRAVE_ENABLE_LOGGING=true
toolrave python server.py
```

Claude Code Example:

```
claude mcp add zen -s user -- ~/Projects/zen-mcp-server/.zen_venv/bin/python ~/Projects/zen-mcp-server/server.py

becomes

claude mcp add zen -s user -- toolrave ~/Projects/zen-mcp-server/.zen_venv/bin/python ~/Projects/zen-mcp-server/server.py
```

## How it works

1. **Client connects** → Tool Rave spawns server, handles handshake, caches response
2. **Client requests tools/list** → Tool Rave spawns server, caches tools list
3. **Client calls tool** → Tool Rave spawns fresh server, replays handshake, forwards call
4. **Multiple tool calls** → Each gets its own server process running in parallel

This enables true parallel execution even for MCP servers that were designed to handle one request at a time.

## Development

```bash
# Install dependencies
uv sync

# Run linting
uv run ruff check .
uv run ruff format .

# Type checking
uv run pyright

# Run tests
uv run pytest
```

## License

MIT
