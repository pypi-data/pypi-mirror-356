"""Open MCP Protocol - Simplified MCP client package."""

from .client import MCPClient
from .llm.anthropic import AnthropicProvider
from .llm.openai import OpenAIProvider

__version__ = "0.1.0"
__all__ = ["MCPClient", "AnthropicProvider", "OpenAIProvider"]