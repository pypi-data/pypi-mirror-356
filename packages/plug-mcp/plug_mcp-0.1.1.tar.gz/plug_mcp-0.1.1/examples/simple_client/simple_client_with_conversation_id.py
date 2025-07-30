#!/usr/bin/env python3
"""
Simple MCP Client with Conversation ID - Basic conversation management example

Shows how to use plug_mcp.client.MCPClient with conversation IDs for maintaining context.
"""

import asyncio
import argparse
import sys
import os

# Add parent directory to path to import plug_mcp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plug_mcp.client import MCPClient


async def main():
    """Simple MCP client with conversation ID example."""
    parser = argparse.ArgumentParser(description="Simple MCP Client with Conversation ID using plug_mcp package")
    parser.add_argument("server", help="Server path (stdio) or URL (HTTP)")
    parser.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable_http"])
    parser.add_argument("--conversation-id", help="Start with specific conversation ID")
    parser.add_argument("--auto-generate", action="store_true", help="Auto-generate conversation IDs for each message")
    
    args = parser.parse_args()
    
    # Create client
    client = MCPClient(
        llm_provider=args.provider,
        model=args.model,
        timeout=30.0,
        conversation_id=args.conversation_id,
        auto_generate_ids=args.auto_generate,
        ssl_verify=False
    )
    
    try:
        # Connect
        print(f"Connecting to {args.server}...")
        await client.connect(args.server, transport=args.transport)
        print("Connected!")
        
        # Show initial conversation state
        conv_id = client.get_conversation_id()
        print(f"Conversation ID: {conv_id}")
        print(f"Auto-generate IDs: {args.auto_generate}")
        
        # Chat loop
        print("\nChat started. Type 'exit' to quit, 'new' to start new conversation, 'history' to show history.")
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() == 'exit':
                    break
                elif user_input.lower() == 'new':
                    # Start new conversation
                    new_conv_id = client.start_conversation()
                    print(f"Started new conversation: {new_conv_id}")
                    continue
                elif user_input.lower() == 'history':
                    # Show conversation history
                    history = client.get_conversation_history()
                    if history:
                        print(f"\nConversation History ({len(history)} messages):")
                        for i, msg in enumerate(history):
                            role = msg.get("role", "unknown")
                            content = msg.get("content", "")
                            if isinstance(content, list):
                                content_str = str(content)
                            else:
                                content_str = str(content)
                            print(f"  {i+1}. {role}: {content_str[:80]}{'...' if len(content_str) > 80 else ''}")
                    else:
                        print("No conversation history yet.")
                    continue
                
                if user_input:
                    print("Assistant: ", end="", flush=True)
                    response = await client.query(user_input)
                    print(response)
                    
                    # Show conversation ID for independent messages
                    current_conv_id = client.get_conversation_id()
                    if current_conv_id and args.auto_generate:
                        print(f"[Conversation ID: {current_conv_id}]")
                    
            except KeyboardInterrupt:
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main()) 