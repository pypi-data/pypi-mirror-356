# joplin-mcp-server

A Model Context Protocol (MCP) stdio server for Joplin, exposing Joplin's local REST API as MCP tools.

- **Tech stack:** Python, uv, httpx, FastMCP
- **License:** MIT

## Features
- Bridges Joplin's REST API to MCP tools
- Designed for extensibility and integration

## Quick Start
1. Clone this repository
2. Set up a Python 3.10+ environment (recommended: `uv`)
3. Install dependencies: `uv pip install -r pyproject.toml`
4. Run the server: `uvx joplin-mcp-server`

## Project Structure
- `src/joplin_mcp_server/` — Main package code
- `specs/` — API documentation and references

## License
MIT
