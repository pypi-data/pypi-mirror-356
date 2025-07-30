#!/usr/bin/env python3
"""
Simple MCP Server Example
A simple MCP server that provides a single tool.
"""

import logging
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("simple_server")


@mcp.tool()
async def hello(name: str) -> str:
    """
    A simple tool that says hello.

    Args:
        name: The name to say hello to.
    """
    logger.info(f"Saying hello to {name}")
    return f"Hello, {name}!"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 