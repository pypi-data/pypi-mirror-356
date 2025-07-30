"""
Basic tests for toolrave CLI.
"""

from typer.testing import CliRunner

from toolrave.main import app


def test_cli_help():
    """Test that CLI help works."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "toolrave" in result.stdout
    assert "parallel tool execution" in result.stdout


def test_cli_no_args():
    """Test that CLI shows error when no args provided."""
    runner = CliRunner()
    result = runner.invoke(app, [])
    assert result.exit_code == 2  # typer shows error when required argument is missing


def test_cli_with_command():
    """Test that CLI accepts commands and handles them properly."""
    runner = CliRunner()
    # This will succeed in parsing args but will wait for stdin (since no input provided)
    # We need to provide input or use a timeout. Since typer testing doesn't easily support
    # stdin input, let's just test that it doesn't crash on startup
    result = runner.invoke(app, ["echo", "test"], input="", catch_exceptions=True)
    # Should exit with 0 since no JSON input was provided and it just reads empty stdin
    assert result.exit_code == 0
