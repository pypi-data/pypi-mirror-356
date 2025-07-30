# MCP Examples

This directory contains various examples demonstrating how to use the `plug_mcp` library.

## 🚀 Quick Start: Simple Client

For users who want to understand how to use the `plug_mcp` package as an MCP client:

```bash
cd simple_client
python simple_client.py --help
```

The Simple Client demonstrates:
- Basic usage of `plug_mcp.client.MCPClient`
- All protocols (stdio, SSE, Streamable HTTP)
- All LLMs (Anthropic Claude, OpenAI GPT)
- Simple command-line interface

**Conversation Management**: Use `simple_client_with_conversation_id.py` for conversation ID and history management.

**Content Safety**: Use `simple_client_with_guardrails.py` for content filtering and safety features.

**[📖 Simple Client Documentation](simple_client/README.md)**

## 📚 Other Examples

### Basic Examples
- `test_client.py` - Enhanced terminal client with transport testing and debugging
- `conversation_example.py` - Demonstrates conversation management
- `independent_messages_example.py` - Shows independent message handling
- `guardrails_example.py` - Examples of using guardrails for content filtering

### Server Examples
- `weather_server_example.py` - Simple weather MCP server
- `sse_mcp_example_server.py` - SSE-based MCP server
- `streamable_mcp_example.py` - Streamable HTTP server example

### Provider-Specific Examples
- `openai_responses_example.py` - OpenAI-specific response handling
- `test_response_block_guardrail.py` - Testing response blocking guardrails

### Utility Examples
- `weather.py` - Weather tool implementation example

## 🎯 Getting Started

1. **For beginners**: Start with the [Simple Client](simple_client/) to understand basic usage
2. **For conversation management**: Use `simple_client_with_conversation_id.py` for context-aware chats
3. **For content safety**: Use `simple_client_with_guardrails.py` for filtering and safety features
4. **For developers**: Check out `test_client.py` for advanced features
5. **For server development**: Look at the server examples
6. **For specific use cases**: Browse the other examples

## 📖 Documentation

Each example includes comments and documentation explaining its purpose and usage. The Simple Client shows the basic pattern for using the `plug_mcp` package.

## 🤝 Contributing

Feel free to add new examples or improve existing ones. Make sure to:
- Include clear documentation
- Follow the existing code style
- Test your examples thoroughly
- Update this README if adding new categories 