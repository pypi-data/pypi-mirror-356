#!/usr/bin/env python3
"""
Simple MCP Client - Basic usage of plug_mcp package

Shows how to use plug_mcp.client.MCPClient for all protocols and LLMs.
"""

import asyncio
import argparse
import sys
import os

# Add parent directory to path to import plug_mcp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plug_mcp.client import MCPClient


async def main():
    """Simple MCP client example."""
    parser = argparse.ArgumentParser(description="Simple MCP Client using plug_mcp package")
    parser.add_argument("server", help="Server path (stdio) or URL (HTTP)")
    parser.add_argument("--provider", choices=["anthropic", "openai"], default="openai")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable_http"])
    
    args = parser.parse_args()
    
    # Create client
    client = MCPClient(
        llm_provider=args.provider,
        model=args.model,
        timeout=30.0,
        ssl_verify=False
    )
    
    try:
        # Connect
        print(f"Connecting to {args.server}...")
        await client.connect(args.server, transport=args.transport)
        print("Connected!")
        
        # Chat loop
        print("\nChat started. Type 'exit' to quit.")
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() == 'exit':
                    break
                
                if user_input:
                    print("Assistant: ", end="", flush=True)
                    response = await client.query(user_input)
                    print(response)
                    
            except KeyboardInterrupt:
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main()) 