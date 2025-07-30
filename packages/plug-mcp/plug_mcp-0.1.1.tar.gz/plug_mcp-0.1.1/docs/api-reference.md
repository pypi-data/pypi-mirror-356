# API Reference

This page provides a reference for the `plug_mcp` library's public API.

## `MCPClient`

The `MCPClient` is the main entry point for interacting with MCP servers.

::: plug_mcp.client.MCPClient
    options:
      show_root_heading: true
      show_source: false

### `__init__`

Initializes the MCP client.

**Parameters:**

*   `llm_provider` (str): The LLM provider to use. Currently supports `"anthropic"` and `"openai"`. Defaults to `"anthropic"`.
*   `env_file` (str, optional): Path to a `.env` file to load environment variables from.
*   `timeout` (float): Default timeout in seconds for operations. Defaults to `30.0`.
*   `conversation_id` (str, optional): An existing conversation ID to resume.
*   `auto_generate_ids` (bool): Whether to automatically generate a unique conversation ID for each message if one isn't active. Defaults to `True`.
*   `**llm_kwargs`: Additional keyword arguments to pass to the LLM provider's constructor.

### `connect`

Connects to an MCP server.

**Parameters:**

*   `connection_string` (str): The connection string for the server (e.g., a URL for HTTP, or a command for STDIO).
*   `transport` (str, optional): The transport protocol to use (`"stdio"`, `"sse"`, `"http"`). If `None`, it's inferred from the connection string.
*   `headers` (dict, optional): A dictionary of headers to use for HTTP-based transports.

### `query`

Sends a message to the AI and gets a response.

**Parameters:**

*   `message` (str): The message to send.
*   `max_iterations` (int): The maximum number of tool-use iterations to perform. Defaults to `5`.
*   `conversation_id` (str, optional): The ID of the conversation to use for this query.

**Returns:**

*   `str`: The AI's response.

### Conversation Management

#### `start_conversation`

Starts a new conversation or resumes an existing one.

**Parameters:**

*   `conversation_id` (str, optional): The ID of the conversation to start or resume. If `None`, a new one is generated.

**Returns:**

*   `str`: The active conversation ID.

#### `get_conversation_history`

Retrieves the message history for the current conversation.

**Returns:**

*   `list`: A list of message dictionaries.

#### `save_conversation` / `load_conversation`

Saves the current conversation state to a file or loads it from a file.

**Parameters:**

*   `filepath` (str): The path to the file.

### Guardrails

#### `add_guardrail`

Adds a guardrail to the client for content moderation.

**Parameters:**

*   `guardrail`: An instance of a guardrail class (e.g., `WordMaskGuardrail`). 