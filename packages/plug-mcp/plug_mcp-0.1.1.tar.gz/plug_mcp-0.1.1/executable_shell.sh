#!/bin/bash

# ==============================================================================
# MCP (Modular Communication Protocol) Example Commands
# ==============================================================================
#
# This script contains a collection of example commands to demonstrate the
# capabilities of the MCP client and server. You can copy and paste these
# commands into your terminal to run them.
#
# For examples that require a server, you will need to run the server command
# in a separate terminal window before running the client command.
#

# ------------------------------------------------------------------------------
# Section 1: Client against a public remote server
# ------------------------------------------------------------------------------
# These examples show how to connect the simple client to a public MCP server
# using different transport protocols.

# Example 1.1: STDIO transport
# Connects using standard input/output.
# python examples/simple_client/simple_client.py https://mcp.deepwiki.com/mcp --model=gpt-4.1 --transport=stdio

# Example 1.2: SSE (Server-Sent Events) transport
# Connects using SSE.
# python examples/simple_client/simple_client.py https://mcp.deepwiki.com/mcp --model=gpt-4.1 --transport=sse

# Example 1.3: Streamable HTTP transport
# Connects using a streamable HTTP connection.
# python examples/simple_client/simple_client.py https://mcp.deepwiki.com/mcp --model=gpt-4.1 --transport=streamable_http


# ------------------------------------------------------------------------------
# Section 2: Local STDIO transport example
# ------------------------------------------------------------------------------
# In this example, the MCP client runs a local Python script as a subprocess
# and communicates with it over STDIO. There is no separate server to run.

# Example 2.1: Client with a local weather tool via STDIO
# The `weather_stdio.py` script acts as the tool provider.
# python examples/simple_client/simple_client.py examples/simple_server/weather_stdio.py --model=claude-3-5-sonnet-20241022 --transport=stdio --provider=anthropic


# ------------------------------------------------------------------------------
# Section 3: Local SSE (Server-Sent Events) example
# ------------------------------------------------------------------------------
# This requires running a local MCP server that uses SSE.

# Step 1: Run the SSE server in a separate terminal
# The server will start and listen on http://localhost:8080/sse
#
# python examples/simple_server/sse_mcp_example_server.py

# Step 2: Run the SSE client in another terminal
# This client will connect to the local SSE server.
#
# python examples/simple_client/simple_client.py http://localhost:8080/sse --model=claude-3-5-sonnet-20241022 --transport=sse --provider=anthropic


# ------------------------------------------------------------------------------
# Section 4: Local Streamable HTTP example
# ------------------------------------------------------------------------------
# This requires running a local MCP server that uses streamable HTTP.

# Step 1: Run the Streamable HTTP server in a separate terminal
# The server will start and listen on http://localhost:8123/mcp
#
# python examples/simple_server/streamable_http_server.py

# Step 2: Run the Streamable HTTP client in another terminal
# This client will connect to the local HTTP server.
#
# python examples/simple_client/simple_client.py http://localhost:8123/mcp --model=claude-3-5-sonnet-20241022 --transport=streamable_http --provider=anthropic


# ------------------------------------------------------------------------------
# Section 5: Advanced Client Features
# ------------------------------------------------------------------------------
# These examples demonstrate advanced features like conversation history and
# guardrails. They use the local Streamable HTTP server from Section 4.
#
# Make sure the Streamable HTTP server is running before trying these commands.
# (See Section 4, Step 1)
#

# Example 5.1: Client with Conversation ID
# This shows how to maintain conversation state by passing a `conversation-id`.
# The server can use this ID to retrieve conversation history.
#
# python examples/simple_client/simple_client_with_conversation_id.py http://localhost:8123/mcp --model=claude-3-5-sonnet-20241022 --transport=streamable_http --provider=anthropic --conversation-id=123

# Example 5.2: Client with Guardrails
# This demonstrates enabling client-side or server-side guardrails.
# The `--enable-all` flag enables all configured guardrails.
#
# python examples/simple_client/simple_client_with_guardrails.py http://localhost:8123/mcp --model=claude-3-5-sonnet-20241022 --transport=streamable_http --provider=anthropic --enable-all