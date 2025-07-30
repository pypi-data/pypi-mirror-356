"""Anthropic Claude provider for MCP."""

import httpx
import logging
import uuid
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class AnthropicProvider:
    """Anthropic Claude provider."""
    
    def __init__(self, api_key=None, model="claude-3-5-sonnet-20241022", ssl_verify=True):
        from anthropic import Anthropic
        
        http_client = httpx.Client(verify=ssl_verify)
        self.client = Anthropic(api_key=api_key, http_client=http_client)
        self.model = model
        self.conversation_id = None
        self.message_history = []
        self.auto_generate_conversation_ids = True

    def start_conversation(self, conversation_id: Optional[str] = None) -> str:
        """Start a new conversation or continue existing one."""
        if conversation_id:
            self.conversation_id = conversation_id
            # Clear message history for new conversation
            self.message_history = []
        else:
            # Generate unique ID for each conversation
            self.conversation_id = str(uuid.uuid4())
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
        logger.info(f"Cleared history for conversation: {self.conversation_id}")

    async def create_completion(self, messages, tools, max_tokens=1000, conversation_id: Optional[str] = None):
        """Create completion with Claude."""
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
            
            # Prepare messages based on conversation mode
            if use_history and self.message_history:
                # Use conversation history
                if len(messages) == 1 and messages[0].get("role") == "user":
                    # New user message, add to history
                    self.add_to_history("user", messages[0]["content"])
                    all_messages = self.message_history
                else:
                    # Multiple messages or different role, use provided messages
                    all_messages = messages
                    # Add to history for future reference
                    for msg in messages:
                        self.add_to_history(msg.get("role", "user"), msg.get("content", ""))
            else:
                # Independent message mode - use only provided messages
                all_messages = messages
                # Add to history for this conversation
                for msg in messages:
                    self.add_to_history(msg.get("role", "user"), msg.get("content", ""))
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=all_messages,
                tools=tools if tools else None
            )
            
            # Add assistant response to history
            self.add_to_history("assistant", response.content)
            
            # Convert response to consistent format
            content_list = []
            for item in response.content:
                if hasattr(item, 'type'):
                    if item.type == 'text':
                        content_list.append({
                            "type": "text",
                            "text": item.text
                        })
                    elif item.type == 'tool_use':
                        content_list.append({
                            "type": "tool_use",
                            "id": item.id,
                            "name": item.name,
                            "input": item.input
                        })
            
            return {
                "content": content_list,
                "model": response.model,
                "conversation_id": self.conversation_id,
                "independent_message": not use_history,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise RuntimeError(f"Anthropic API error: {e}")

    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation data for persistence."""
        return {
            "conversation_id": self.conversation_id,
            "message_history": self.message_history.copy(),
            "model": self.model
        }

    def import_conversation(self, conversation_data: Dict[str, Any]):
        """Import conversation data from persistence."""
        self.conversation_id = conversation_data.get("conversation_id")
        self.message_history = conversation_data.get("message_history", [])
        self.model = conversation_data.get("model", self.model)
        logger.info(f"Imported conversation: {self.conversation_id}")

    def set_auto_generate_conversation_ids(self, enabled: bool):
        """Enable or disable automatic conversation ID generation."""
        self.auto_generate_conversation_ids = enabled
        logger.info(f"Auto-generate conversation IDs: {enabled}")