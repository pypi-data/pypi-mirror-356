"""
entry.py
A FastMCP server entry point for listing Joplin folders.
"""

import os

from fastmcp import FastMCP

from .joplin_client import JoplinClient

mcp = FastMCP(name="Joplin MCP Server")

# Get token from environment variable for security
JOPLIN_TOKEN = os.environ.get("JOPLIN_TOKEN", "")
joplin = JoplinClient(base_url="http://localhost:41184", token=JOPLIN_TOKEN)


@mcp.tool
async def list_folders() -> dict:
    """List all Joplin folders (notebooks) using the Joplin API."""

    return await joplin.get_folders()


def main():
    mcp.run()


if __name__ == "__main__":
    main()
