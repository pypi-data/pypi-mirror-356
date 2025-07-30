"""Main MCP client with simplified interface."""

import asyncio
import logging
import json
import os
from contextlib import AsyncExitStack
from typing import Optional, Dict, Any, List
from .transport import TransportManager
from .llm.anthropic import AnthropicProvider
from .llm.openai import OpenAIProvider
from .utils import load_env_vars, run_with_timeout, format_tool_for_llm
from .guardrails import GuardrailManager, WordMaskGuardrail, PIIGuardrail, InjectionGuardrail

logger = logging.getLogger(__name__)


class MCPClient:
    """Simplified MCP client."""
    
    def __init__(self, llm_provider="anthropic", env_file=None, timeout=30.0, conversation_id=None, auto_generate_ids=True, **llm_kwargs):
        load_env_vars(env_file)
        
        self.timeout = timeout
        self.exit_stack = AsyncExitStack()
        self.transport = TransportManager(self.exit_stack, timeout)
        self._tools_cache = []
        self._connected = False
        self.conversation_id = conversation_id
        self.auto_generate_ids = auto_generate_ids
        
        # Initialize guardrails
        self.guardrails = GuardrailManager()
        
        # Initialize LLM provider
        if llm_provider == "anthropic":
            self.llm = AnthropicProvider(**llm_kwargs)
        elif llm_provider == "openai":
            self.llm = OpenAIProvider(**llm_kwargs)
        else:
            raise ValueError(f"Unknown LLM provider: {llm_provider}")
        
        # Configure auto-generation behavior
        self.llm.set_auto_generate_conversation_ids(auto_generate_ids)
        
        # Start conversation if ID provided
        if conversation_id:
            self.llm.start_conversation(conversation_id)

    def add_guardrail(self, guardrail):
        """Add a guardrail to the client."""
        self.guardrails.add_guardrail(guardrail)
        logger.info(f"Added guardrail: {guardrail.name}")

    def start_conversation(self, conversation_id: Optional[str] = None) -> str:
        """Start a new conversation or continue existing one."""
        self.conversation_id = self.llm.start_conversation(conversation_id)
        logger.info(f"Started conversation: {self.conversation_id}")
        return self.conversation_id

    def get_conversation_id(self) -> Optional[str]:
        """Get current conversation ID."""
        return self.llm.get_conversation_id()

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.llm.get_history()

    def clear_conversation_history(self):
        """Clear conversation history."""
        self.llm.clear_history()
        logger.info("Cleared conversation history")

    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation data for persistence."""
        return self.llm.export_conversation()

    def import_conversation(self, conversation_data: Dict[str, Any]):
        """Import conversation data from persistence."""
        self.llm.import_conversation(conversation_data)
        self.conversation_id = self.llm.get_conversation_id()

    def save_conversation(self, filepath: str):
        """Save conversation to file."""
        conversation_data = self.export_conversation()
        with open(filepath, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        logger.info(f"Saved conversation to {filepath}")

    def load_conversation(self, filepath: str):
        """Load conversation from file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Conversation file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            conversation_data = json.load(f)
        
        self.import_conversation(conversation_data)
        logger.info(f"Loaded conversation from {filepath}")

    def set_auto_generate_conversation_ids(self, enabled: bool):
        """Enable or disable automatic conversation ID generation for independent messages."""
        self.auto_generate_ids = enabled
        self.llm.set_auto_generate_conversation_ids(enabled)
        logger.info(f"Auto-generate conversation IDs: {enabled}")

    async def connect(self, connection_string, transport=None, headers=None, **kwargs):
        """Connect to MCP server."""
        if self._connected:
            await self.disconnect()
        
        # Handle OpenAI provider differently
        if isinstance(self.llm, OpenAIProvider):
            if transport == "stdio":
                raise ValueError("OpenAI provider doesn't support STDIO transport")
            
            server_label = kwargs.get('server_label', 'default_server')
            self.llm.add_mcp_server(connection_string, server_label, **kwargs)
            self._connected = True
            logger.info(f"OpenAI MCP server configured: {connection_string}")
            return
        
        # Anthropic provider - use transport manager
        self.session = await self.transport.connect(connection_string, transport, headers)
        await self._refresh_tools()
        self._connected = True
        logger.info(f"Connected via {self.transport.get_type()}")

    async def _refresh_tools(self):
        """Refresh tools from server."""
        if not self.session:
            return
        
        try:
            response = await run_with_timeout(self.session.list_tools(), self.timeout)
            if hasattr(response, 'tools'):
                self._tools_cache = [format_tool_for_llm(tool) for tool in response.tools]
                logger.info(f"Loaded {len(self._tools_cache)} tools")
        except Exception as e:
            logger.error(f"Failed to refresh tools: {e}")
            self._tools_cache = []

    async def query(self, message, max_iterations=5, conversation_id: Optional[str] = None):
        """Process query with LLM and tools."""
        if not self._connected:
            raise RuntimeError("Not connected. Call connect() first.")
        
        # Handle conversation ID logic
        if conversation_id:
            # User provided conversation ID - use it
            self.start_conversation(conversation_id)
        elif not self.get_conversation_id() and self.auto_generate_ids:
            # No conversation ID and auto-generation enabled - generate unique ID for this message
            self.start_conversation()
            logger.info(f"Generated unique conversation ID for independent message: {self.get_conversation_id()}")
        
        # Run guardrails on input message
        guardrail_results = await self.guardrails.check_all(message)
        for result in guardrail_results:
            if not result.passed:
                logger.warning(f"Guardrail check failed: {result.message}")
                if result.masked_content:
                    message = result.masked_content
        
        # OpenAI provider handling
        if isinstance(self.llm, OpenAIProvider):
            response = await run_with_timeout(
                self.llm.create_completion([{"role": "user", "content": message}], [], conversation_id=self.get_conversation_id()),
                self.timeout
            )
            
            # Handle approvals if needed
            if response.get("requires_approval"):
                for approval in response.get("approval_requests", []):
                    response = await run_with_timeout(
                        self.llm.handle_approval(approval["id"], True),
                        self.timeout
                    )
            
            content = response.get("content", [])
            response_text = content[0].get("text", "No response") if content else "No response"
            
            # Run guardrails on response
            guardrail_results = await self.guardrails.check_all(response_text)
            for result in guardrail_results:
                if not result.passed:
                    logger.warning(f"Guardrail check failed on response: {result.message}")
                    if result.masked_content:
                        response_text = result.masked_content
            
            return response_text
        
        # Anthropic provider handling
        messages = [{"role": "user", "content": message}]
        
        for iteration in range(max_iterations):
            response = await run_with_timeout(
                self.llm.create_completion(messages, self._tools_cache, conversation_id=self.get_conversation_id()),
                self.timeout
            )
            
            # Extract text content and apply guardrails
            text_content = []
            for item in response["content"]:
                if item.get("type") == "text":
                    # Apply guardrails to each text segment
                    guardrail_results = await self.guardrails.check_all(item["text"])
                    for result in guardrail_results:
                        if not result.passed:
                            logger.warning(f"Guardrail check failed on response segment: {result.message}")
                            if result.masked_content:
                                item["text"] = result.masked_content
                    text_content.append(item["text"])
            
            messages.append({"role": "assistant", "content": response["content"]})
            
            # Check for tool calls
            tool_calls = [item for item in response["content"] if item.get("type") == "tool_use"]
            
            if not tool_calls:
                return " ".join(text_content)
            
            # Execute tools
            tool_results = []
            for tool_call in tool_calls:
                try:
                    result = await run_with_timeout(
                        self.session.call_tool(tool_call["name"], tool_call["input"]),
                        self.timeout
                    )
                    # Apply guardrails to tool results
                    guardrail_results = await self.guardrails.check_all(result.content)
                    masked_content = result.content
                    for guardrail_result in guardrail_results:
                        if not guardrail_result.passed and guardrail_result.masked_content:
                            masked_content = guardrail_result.masked_content
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_call["id"],
                        "content": masked_content
                    })
                except Exception as e:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_call["id"],
                        "content": f"Error: {str(e)}",
                        "is_error": True
                    })
            
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
        
        raise RuntimeError(f"Query exceeded {max_iterations} iterations")

    async def list_tools(self):
        """Get available tools."""
        if isinstance(self.llm, OpenAIProvider):
            return []  # OpenAI tools are managed by Responses API
        
        if not self._connected:
            return []
        
        await self._refresh_tools()
        return self._tools_cache.copy()

    async def call_tool(self, tool_name, tool_args):
        """Call tool directly."""
        if isinstance(self.llm, OpenAIProvider):
            raise RuntimeError("Direct tool calls not supported with OpenAI provider")
        
        if not self._connected or not self.session:
            raise RuntimeError("Not connected")
        
        result = await run_with_timeout(
            self.session.call_tool(tool_name, tool_args),
            self.timeout
        )
        return result.content

    async def disconnect(self):
        """Disconnect from server."""
        if isinstance(self.llm, OpenAIProvider):
            self.llm.clear_mcp_servers()
        else:
            await self.exit_stack.aclose()
            self.exit_stack = AsyncExitStack()
            self.transport = TransportManager(self.exit_stack, self.timeout)
        
        self._connected = False
        self._tools_cache = []
        logger.info("Disconnected")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    def get_debug_info(self):
        """Get debug information about the client's current state.
        
        Returns:
            dict: A dictionary containing debug information including:
                - connected: Whether the client is connected
                - transport_type: Current transport type (stdio/sse/streamable_http)
                - llm_provider: Name of the LLM provider class
                - tools_count: Number of tools in cache
                - connection_string: Current connection string
                - timeout: Current timeout setting
                - conversation_id: Current conversation ID
                - history_length: Number of messages in conversation history
                - auto_generate_ids: Whether auto-generation is enabled
        """
        return {
            "connected": self._connected,
            "transport_type": self.transport.get_type() if hasattr(self, 'transport') else None,
            "llm_provider": self.llm.__class__.__name__,
            "tools_count": len(self._tools_cache),
            "connection_string": self.transport.get_connection_string() if hasattr(self, 'transport') else None,
            "timeout": self.timeout,
            "conversation_id": self.get_conversation_id(),
            "history_length": len(self.get_conversation_history()),
            "auto_generate_ids": self.auto_generate_ids
        }

    def is_connected(self):
        return self._connected