"""
Main CLI entry point for toolrave.
"""

from typing import Annotated

import typer

from .proxy import MCPProxy

app = typer.Typer(
    name="toolrave",
    help="Universal MCP server proxy that enables parallel tool execution",
    no_args_is_help=True,
)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def main(
    ctx: typer.Context,
    command: Annotated[
        list[str],
        typer.Argument(
            help="MCP server command and arguments (e.g., 'python server.py --flag value')"
        ),
    ],
) -> None:
    """
    Run an MCP server through the toolrave proxy for parallel tool execution.

    Example:
        toolrave python server.py
        toolrave python server.py --some-flag value
        toolrave uv run server.py
    """
    if not command:
        typer.echo("Error: No command provided", err=True)
        raise typer.Exit(1)

    # Combine command with any extra args from context
    full_command = list(command) + ctx.args

    try:
        proxy = MCPProxy(full_command)
        proxy.run()
    except KeyboardInterrupt:
        typer.echo("\nShutdown requested by user", err=True)
        raise typer.Exit(0) from None
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
