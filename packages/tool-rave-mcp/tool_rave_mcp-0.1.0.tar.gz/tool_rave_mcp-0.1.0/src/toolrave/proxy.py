"""
Core MCP proxy logic for parallel tool execution.
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any


class MCPProxy:
    """
    MCP server proxy that enables parallel tool execution.

    This proxy works by:
    1. Caching the handshake sequence
    2. Caching discovery responses (tools/list, prompts/list, resources/list)
    3. Spawning fresh server processes for each tool call
    """

    def __init__(self, server_command: list[str]):
        self.server_command = server_command
        self.max_workers = int(os.getenv("TOOLRAVE_MAX_WORKERS", "8"))
        self.log_dir = os.getenv("TOOLRAVE_LOG_DIR", str(Path.home() / ".toolrave" / "logs"))
        self.enable_logging = os.getenv("TOOLRAVE_ENABLE_LOGGING", "false").lower() == "true"

        # Ensure log directory exists if logging is enabled
        if self.enable_logging:
            Path(self.log_dir).mkdir(parents=True, exist_ok=True)
            log_file = Path(self.log_dir) / f"toolrave_{time.strftime('%Y%m%d_%H%M%S')}.log"
            self._log_file = open(log_file, "a", buffering=1)
        else:
            self._log_file = None

        self._log_lock = threading.Lock()

        # State
        self.handshake: list[str] = []
        self.discovery_cache: dict[str, Any] | None = None

        # Worker pool
        self.call_queue: queue.Queue[str] = queue.Queue()
        self._workers = []
        self._start_workers()

    def _log(self, tag: str, text: str) -> None:
        """Log message if logging is enabled."""
        if self._log_file:
            with self._log_lock:
                self._log_file.write(f"{tag}: {text.rstrip()}\n")

    def _start_workers(self) -> None:
        """Start worker threads for tool calls."""
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self._workers.append(worker)

    def _worker(self) -> None:
        """Worker thread that processes tool calls."""
        while True:
            raw = self.call_queue.get()
            if raw is None:  # Shutdown signal
                break

            try:
                call_id = json.loads(raw).get("id")
            except Exception:
                call_id = None

            self._log("SPAWN", f"spawning server for tool call id={call_id}")

            try:
                child = subprocess.Popen(
                    self.server_command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                # Replay handshake
                for line in self.handshake:
                    child.stdin.write(line)

                # Forward the call
                child.stdin.write(raw)
                child.stdin.flush()

                # Read response
                reply = self._read_until_id(child, call_id)
                sys.stdout.write(reply)
                sys.stdout.flush()
                self._log("OUT", reply)

                child.terminate()
                child.wait(timeout=5)  # Give it time to terminate gracefully

            except Exception as e:
                self._log("ERROR", f"Worker error for call {call_id}: {e}")
                # Send error response
                error_response = {
                    "jsonrpc": "2.0",
                    "id": call_id,
                    "error": {"code": -32603, "message": f"Internal error: {e}"},
                }
                error_line = json.dumps(error_response) + "\n"
                sys.stdout.write(error_line)
                sys.stdout.flush()
                self._log("OUT", error_line)

            finally:
                self.call_queue.task_done()

    def _read_until_id(self, child: subprocess.Popen, want_id: Any) -> str:
        """
        Read from child stdout until we see a JSON object with matching id.
        Forward any other output (notifications) upstream.
        """
        while True:
            line = child.stdout.readline()
            if not line:
                raise RuntimeError(f"child exited before answering id {want_id}")

            try:
                if json.loads(line).get("id") == want_id:
                    return line
            except Exception:
                pass

            # Forward non-matching output (notifications etc.)
            sys.stdout.write(line)
            sys.stdout.flush()
            self._log("OUT", line)

    def _handle_initialize(self, line: str, msg: dict[str, Any]) -> None:
        """Handle initialize request by spawning server and caching response."""
        self.handshake.append(line)
        self._log("SPAWN", "spawning server for initialize handshake")

        child = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        child.stdin.write(line)
        child.stdin.flush()

        reply = self._read_until_id(child, msg["id"])
        sys.stdout.write(reply)
        sys.stdout.flush()
        self._log("OUT", reply)

        child.terminate()
        child.wait(timeout=5)

    def _handle_discovery(self, line: str, msg: dict[str, Any], method: str) -> None:
        """Handle discovery requests (tools/list, prompts/list, resources/list)."""
        if self.discovery_cache is None:
            self._log("SPAWN", f"spawning server for discovery cache ({method})")

            child = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Replay handshake
            for handshake_line in self.handshake:
                child.stdin.write(handshake_line)

            child.stdin.write(line)
            child.stdin.flush()

            raw = self._read_until_id(child, msg["id"])
            self.discovery_cache = json.loads(raw)
            child.terminate()
            child.wait(timeout=5)
        else:
            # Use cached response with new id
            self.discovery_cache["id"] = msg["id"]
            raw = json.dumps(self.discovery_cache) + "\n"

        sys.stdout.write(raw)
        sys.stdout.flush()
        self._log("OUT", raw)

    def run(self) -> None:
        """Main proxy loop."""
        self._log("START", f"Starting toolrave proxy for command: {' '.join(self.server_command)}")

        try:
            for line in sys.stdin:
                self._log("IN", line)

                try:
                    msg = json.loads(line)
                except Exception:
                    # Non-JSON input, just forward it
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    continue

                method = msg.get("method")

                # Handle different message types
                if method == "initialize":
                    self._handle_initialize(line, msg)
                elif method == "notifications/initialized":
                    self.handshake.append(line)
                elif method in ("tools/list", "prompts/list", "resources/list"):
                    self._handle_discovery(line, msg, method)
                elif method == "tools/call":
                    self.call_queue.put(line)
                else:
                    # Unknown method - send error
                    error = {
                        "jsonrpc": "2.0",
                        "id": msg.get("id"),
                        "error": {"code": -32601, "message": f"Unhandled method {method}"},
                    }
                    error_line = json.dumps(error) + "\n"
                    sys.stdout.write(error_line)
                    sys.stdout.flush()
                    self._log("OUT", error_line)

        finally:
            self._shutdown()

    def _shutdown(self) -> None:
        """Clean shutdown of workers and resources."""
        self._log("SHUTDOWN", "Shutting down proxy")

        # Signal workers to stop
        for _ in self._workers:
            self.call_queue.put(None)

        # Wait for workers to finish
        for worker in self._workers:
            worker.join(timeout=5)

        if self._log_file:
            self._log_file.close()
