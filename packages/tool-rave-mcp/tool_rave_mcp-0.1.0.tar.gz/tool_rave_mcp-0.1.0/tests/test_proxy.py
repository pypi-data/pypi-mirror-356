"""
Tests for MCPProxy class.
"""

from unittest.mock import patch

import pytest

from toolrave.proxy import MCPProxy


def test_proxy_init():
    """Test proxy initialization."""
    proxy = MCPProxy(["echo", "test"])
    assert proxy.server_command == ["echo", "test"]
    assert proxy.max_workers == 8  # default
    assert proxy.handshake == []
    assert proxy.discovery_cache is None


def test_proxy_with_env_vars():
    """Test proxy initialization with environment variables."""
    with patch.dict(
        "os.environ", {"TOOLRAVE_MAX_WORKERS": "16", "TOOLRAVE_ENABLE_LOGGING": "true"}
    ):
        proxy = MCPProxy(["python", "server.py"])
        assert proxy.max_workers == 16
        assert proxy._log_file is not None


def test_log_disabled_by_default():
    """Test that logging is disabled by default."""
    proxy = MCPProxy(["echo", "test"])
    assert proxy._log_file is None

    # Should not raise any errors
    proxy._log("TEST", "message")


@pytest.fixture
def mock_proxy():
    """Create a proxy with mocked subprocess for testing."""
    with patch("toolrave.proxy.subprocess.Popen") as mock_popen:
        proxy = MCPProxy(["echo", "test"])
        yield proxy, mock_popen
