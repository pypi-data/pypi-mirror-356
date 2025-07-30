"""Utility functions for MCP client."""

import os
import asyncio
from pathlib import Path
from urllib.parse import urlparse


def load_env_vars(env_file=None):
    """Load environment variables from file."""
    if env_file and os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value


def validate_server_path(server_path):
    """Validate server path exists."""
    return os.path.exists(server_path) or os.path.exists(server_path.split()[0])


def get_server_command(server_path):
    """Parse server command and arguments."""
    parts = server_path.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    
    # Handle Python scripts
    if command.endswith('.py'):
        return 'python', [command] + args
    
    return command, args


def is_valid_url(url):
    """Check if string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


async def run_with_timeout(coro, timeout):
    """Run coroutine with timeout."""
    return await asyncio.wait_for(coro, timeout=timeout)


def format_tool_for_llm(tool):
    """Format MCP tool for LLM consumption."""
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.inputSchema
    }