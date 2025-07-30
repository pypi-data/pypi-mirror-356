"""OpenAI provider for MCP using Responses API."""

import httpx
import logging
import uuid
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class OpenAIProvider:
    """OpenAI provider with MCP support via Responses API."""
    
    def __init__(self, api_key=None, model="gpt-4.1", ssl_verify=True):
        from openai import OpenAI
        
        http_client = httpx.Client(verify=ssl_verify)
        self.client = OpenAI(api_key=api_key, http_client=http_client)
        self.model = model
        self._mcp_servers = []
        self._previous_response_id = None
        self.conversation_id = None
        self.message_history = []
        self.auto_generate_conversation_ids = True

    def start_conversation(self, conversation_id: Optional[str] = None) -> str:
        """Start a new conversation or continue existing one."""
        if conversation_id:
            self.conversation_id = conversation_id
            # Clear response ID for new conversation
            self._previous_response_id = None
            self.message_history = []
        else:
            # Generate unique ID for each conversation
            self.conversation_id = str(uuid.uuid4())
            self._previous_response_id = None
            self.message_history = []
        
        logger.info(f"Started conversation: {self.conversation_id}")
        return self.conversation_id

    def get_conversation_id(self) -> Optional[str]:
        """Get current conversation ID."""
        return self.conversation_id

    def add_to_history(self, role: str, content: Any):
        """Add message to conversation history."""
        if not self.conversation_id:
            self.start_conversation()
        
        self.message_history.append({
            "role": role,
            "content": content
        })
        logger.debug(f"Added {role} message to conversation {self.conversation_id}")

    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.message_history.copy()

    def clear_history(self):
        """Clear conversation history."""
        self.message_history = []
        self._previous_response_id = None
        logger.info(f"Cleared history for conversation: {self.conversation_id}")

    def add_mcp_server(self, server_url, server_label, require_approval="always", allowed_tools=None, **kwargs):
        """Add MCP server configuration."""
        server_config = {
            "type": "mcp",
            "server_url": server_url,
            "server_label": server_label,
            "require_approval": require_approval
        }
        
        if allowed_tools:
            server_config["allowed_tools"] = allowed_tools
        
        self._mcp_servers.append(server_config)
        logger.info(f"Added MCP server: {server_label} at {server_url}")

    def _get_item_type(self, item):
        """Get item type from response."""
        if hasattr(item, 'type'):
            return item.type
        elif isinstance(item, dict):
            return item.get('type')
        else:
            class_name = item.__class__.__name__.lower()
            if 'approval' in class_name:
                return 'mcp_approval_request'
            elif 'call' in class_name:
                return 'mcp_call'
            elif 'text' in class_name:
                return 'text'
            return 'unknown'

    def _extract_attr(self, item, attr, default=None):
        """Extract attribute from item."""
        if hasattr(item, attr):
            return getattr(item, attr)
        elif isinstance(item, dict):
            return item.get(attr, default)
        return default

    async def create_completion(self, messages, tools, max_tokens=None, user_input=None, conversation_id: Optional[str] = None):
        """Create completion with OpenAI Responses API."""
        try:
            # Handle conversation ID logic
            if conversation_id:
                # User provided conversation ID - use it and maintain history
                self.start_conversation(conversation_id)
                use_history = True
            elif self.conversation_id and self.message_history:
                # Existing conversation - continue with history
                use_history = True
            else:
                # No conversation ID provided and no existing conversation
                # Generate unique ID for this message (treat as independent conversation)
                self.start_conversation()
                use_history = False
                logger.info(f"Generated unique conversation ID for independent message: {self.conversation_id}")
            
            # Extract user input if not provided
            if user_input is None:
                user_messages = [msg for msg in messages if msg.get("role") == "user"]
                if user_messages:
                    last_msg = user_messages[-1]
                    user_input = last_msg.get("content", "")
                    if isinstance(user_input, list):
                        text_parts = [item.get("text", "") for item in user_input if item.get("type") == "text"]
                        user_input = " ".join(text_parts)
                else:
                    user_input = ""
            
            # Add user message to history
            self.add_to_history("user", user_input)
            
            # Prepare request
            request_params = {
                "model": self.model,
                "input": user_input,
                "tools": self._mcp_servers
            }
            
            if max_tokens:
                request_params["max_tokens"] = max_tokens
            
            # Only use previous_response_id if we're in conversation mode
            if use_history and self._previous_response_id:
                request_params["previous_response_id"] = self._previous_response_id
            
            # Create response
            response = self.client.responses.create(**request_params)
            self._previous_response_id = response.id
            
            # Check for approval requests
            approval_requests = []
            for item in response.output:
                if self._get_item_type(item) == "mcp_approval_request":
                    approval_requests.append({
                        "id": self._extract_attr(item, "id"),
                        "type": "mcp_approval_request",
                        "name": self._extract_attr(item, "name"),
                        "arguments": self._extract_attr(item, "arguments"),
                        "server_label": self._extract_attr(item, "server_label")
                    })
            
            if approval_requests:
                return {
                    "content": [{"type": "text", "text": "Approval required for MCP tool calls"}],
                    "model": response.model,
                    "conversation_id": self.conversation_id,
                    "independent_message": not use_history,
                    "approval_requests": approval_requests,
                    "response_id": response.id,
                    "requires_approval": True
                }
            
            # Extract text and MCP calls
            text_parts = []
            mcp_calls = []
            
            for item in response.output:
                item_type = self._get_item_type(item)
                
                if item_type == "text":
                    content = self._extract_attr(item, "content", "")
                    if content:
                        text_parts.append(content)
                elif item_type == "mcp_call":
                    call_info = {
                        "id": self._extract_attr(item, "id"),
                        "name": self._extract_attr(item, "name"),
                        "arguments": self._extract_attr(item, "arguments"),
                        "output": self._extract_attr(item, "output"),
                        "error": self._extract_attr(item, "error"),
                        "server_label": self._extract_attr(item, "server_label")
                    }
                    mcp_calls.append(call_info)
                    
                    # Add tool output to text
                    tool_output = call_info.get("output", "")
                    if tool_output:
                        text_parts.append(f"[Tool '{call_info.get('name')}': {tool_output}]")
            
            # Get final text
            final_text = getattr(response, 'output_text', None) or " ".join(text_parts)
            if not final_text.strip():
                final_text = "Hello! How can I help you today?"
            
            # Add assistant response to history
            self.add_to_history("assistant", final_text)
            
            return {
                "content": [{"type": "text", "text": final_text}],
                "model": response.model,
                "conversation_id": self.conversation_id,
                "independent_message": not use_history,
                "mcp_calls": mcp_calls,
                "response_id": response.id,
                "requires_approval": False,
                "output_text": final_text
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise RuntimeError(f"OpenAI API error: {e}")

    async def handle_approval(self, approval_request_id, approve=True):
        """Handle MCP tool approval."""
        try:
            if not self._previous_response_id:
                raise ValueError("No previous response ID for approval")
            
            response = self.client.responses.create(
                model=self.model,
                tools=self._mcp_servers,
                previous_response_id=self._previous_response_id,
                input=[{
                    "type": "mcp_approval_response",
                    "approve": approve,
                    "approval_request_id": approval_request_id
                }]
            )
            
            self._previous_response_id = response.id
            
            # Process response
            text_parts = []
            mcp_calls = []
            
            for item in response.output:
                item_type = self._get_item_type(item)
                
                if item_type == "text":
                    content = self._extract_attr(item, "content", "")
                    if content:
                        text_parts.append(content)
                elif item_type == "mcp_call":
                    call_info = {
                        "id": self._extract_attr(item, "id"),
                        "name": self._extract_attr(item, "name"),
                        "output": self._extract_attr(item, "output"),
                        "error": self._extract_attr(item, "error")
                    }
                    mcp_calls.append(call_info)
                    
                    tool_output = call_info.get("output", "")
                    if tool_output:
                        text_parts.append(f"[Tool '{call_info.get('name')}': {tool_output}]")
            
            final_text = getattr(response, 'output_text', None) or " ".join(text_parts)
            
            # Add assistant response to history
            self.add_to_history("assistant", final_text)
            
            return {
                "content": [{"type": "text", "text": final_text}],
                "model": response.model,
                "conversation_id": self.conversation_id,
                "mcp_calls": mcp_calls,
                "response_id": response.id,
                "requires_approval": False,
                "output_text": final_text
            }
            
        except Exception as e:
            logger.error(f"OpenAI approval error: {e}")
            raise RuntimeError(f"OpenAI approval error: {e}")

    def clear_mcp_servers(self):
        """Clear all MCP servers."""
        self._mcp_servers = []
        self._previous_response_id = None
        logger.info("Cleared all MCP servers")

    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation data for persistence."""
        return {
            "conversation_id": self.conversation_id,
            "message_history": self.message_history.copy(),
            "model": self.model,
            "previous_response_id": self._previous_response_id
        }

    def import_conversation(self, conversation_data: Dict[str, Any]):
        """Import conversation data from persistence."""
        self.conversation_id = conversation_data.get("conversation_id")
        self.message_history = conversation_data.get("message_history", [])
        self.model = conversation_data.get("model", self.model)
        self._previous_response_id = conversation_data.get("previous_response_id")
        logger.info(f"Imported conversation: {self.conversation_id}")

    def set_auto_generate_conversation_ids(self, enabled: bool):
        """Enable or disable automatic conversation ID generation."""
        self.auto_generate_conversation_ids = enabled
        logger.info(f"Auto-generate conversation IDs: {enabled}")