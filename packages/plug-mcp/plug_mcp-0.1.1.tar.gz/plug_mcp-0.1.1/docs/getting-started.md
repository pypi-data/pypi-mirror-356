# Getting Started

This guide will help you get up and running with `plug_mcp`.

## Installation

To install `plug_mcp`, run the following command in your terminal:

```bash
pip install plug_mcp
```

This will install the core library and its dependencies.

## Quick Start

Here's a simple example of how to use `plug_mcp` to connect to an MCP server and interact with an AI model:

```python
import asyncio
from plug_mcp.client import MCPClient

async def main():
    # Connect to a local server using STDIO
    client = MCPClient(llm_provider="anthropic")
    await client.connect("python examples/simple_server/main.py")

    # Start a conversation
    conversation_id = client.start_conversation()
    print(f"Started conversation: {conversation_id}")

    # Send a message and get a response
    response = await client.query("Hello, world!")
    print(f"AI: {response}")

    # Disconnect from the server
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

This example demonstrates the basic workflow:

1.  **Import `MCPClient`**: The main entry point for interacting with the library.
2.  **Instantiate the client**: Create an instance of `MCPClient`, specifying the desired LLM provider.
3.  **Connect to a server**: Use `await client.connect()` to establish a connection.
4.  **Interact with the AI**: Use methods like `start_conversation()` and `query()` to have a conversation.
5.  **Disconnect**: Cleanly close the connection with `await client.disconnect()`.

For more detailed examples, please refer to the `examples` directory in the [project repository](https://github.com/2796gaurav/plug_mcp). 