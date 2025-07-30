"""Transport layer management for MCP connections."""

import asyncio
import logging
from urllib.parse import urlparse
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from .utils import validate_server_path, get_server_command, is_valid_url, run_with_timeout

logger = logging.getLogger(__name__)


class TransportManager:
    """Manages different MCP transport protocols."""
    
    def __init__(self, exit_stack, timeout=30.0):
        self.exit_stack = exit_stack
        self.timeout = timeout
        self._transport_type = None
        self._connection_string = None

    async def connect(self, connection_string, transport=None, headers=None):
        """Connect using appropriate transport."""
        self._connection_string = connection_string
        
        # Auto-detect transport if not specified
        if transport is None:
            transport = "stdio" if not is_valid_url(connection_string) else "streamable_http"
        
        transport = transport.lower()
        
        if transport == "stdio":
            return await self._connect_stdio(connection_string)
        elif transport == "sse":
            return await self._connect_sse(connection_string, headers)
        elif transport == "streamable_http":
            return await self._connect_streamable_http(connection_string, headers)
        else:
            raise ValueError(f"Unsupported transport: {transport}")

    async def _connect_stdio(self, server_path):
        """Connect via STDIO transport."""
        if not validate_server_path(server_path):
            raise ValueError(f"Invalid server path: {server_path}")
        
        command, args = get_server_command(server_path)
        logger.info(f"Starting STDIO server: {command} {' '.join(args)}")
        
        server_params = StdioServerParameters(command=command, args=args, env=None)
        read_stream, write_stream = await run_with_timeout(
            self.exit_stack.enter_async_context(stdio_client(server_params)),
            self.timeout
        )
        
        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        
        await run_with_timeout(session.initialize(), self.timeout)
        self._transport_type = "stdio"
        logger.info(f"STDIO connection established: {server_path}")
        return session

    async def _connect_sse(self, server_url, headers=None):
        """Connect via SSE transport."""
        parsed = urlparse(server_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid SSE URL: {server_url}")
        
        logger.info(f"Connecting to SSE server: {server_url}")
        
        read_stream, write_stream = await run_with_timeout(
            self.exit_stack.enter_async_context(
                sse_client(url=server_url, headers=headers or {})
            ),
            self.timeout
        )
        
        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        
        await run_with_timeout(session.initialize(), min(15.0, self.timeout))
        self._transport_type = "sse"
        logger.info(f"SSE connection established: {server_url}")
        return session

    async def _connect_streamable_http(self, server_url, headers=None):
        """Connect via Streamable HTTP transport."""
        parsed = urlparse(server_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid HTTP URL: {server_url}")
        
        logger.info(f"Connecting to HTTP server: {server_url}")
        
        read_stream, write_stream, metadata = await run_with_timeout(
            self.exit_stack.enter_async_context(
                streamablehttp_client(url=server_url, headers=headers or {})
            ),
            self.timeout
        )
        
        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        
        await run_with_timeout(session.initialize(), min(15.0, self.timeout))
        self._transport_type = "streamable_http"
        logger.info(f"HTTP connection established: {server_url}")
        return session

    def get_type(self):
        """Get current transport type."""
        return self._transport_type

    def get_connection_string(self):
        """Get current connection string."""
        return self._connection_string