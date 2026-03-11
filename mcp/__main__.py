"""Entry point for running the MCP server: python -m mcp"""

from __future__ import annotations

from mcp.server import run_stdio

if __name__ == "__main__":
    run_stdio()
