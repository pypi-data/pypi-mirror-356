#!/usr/bin/env python3
"""
Simple MCP Client with Guardrails - Basic guardrails example

Shows how to use plug_mcp.client.MCPClient with guardrails for content filtering and safety.
"""

import asyncio
import argparse
import sys
import os

# Add parent directory to path to import plug_mcp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plug_mcp.client import MCPClient
from plug_mcp.guardrails import (
    WordMaskGuardrail, 
    PIIGuardrail, 
    InjectionGuardrail, 
    ResponseBlockGuardrail
)


async def main():
    """Simple MCP client with guardrails example."""
    parser = argparse.ArgumentParser(description="Simple MCP Client with Guardrails using plug_mcp package")
    parser.add_argument("server", help="Server path (stdio) or URL (HTTP)")
    parser.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable_http"])
    parser.add_argument("--enable-word-mask", action="store_true", help="Enable word masking guardrail")
    parser.add_argument("--enable-pii", action="store_true", help="Enable PII detection guardrail")
    parser.add_argument("--enable-injection", action="store_true", help="Enable injection detection guardrail")
    parser.add_argument("--enable-response-block", action="store_true", help="Enable response blocking guardrail")
    parser.add_argument("--enable-all", action="store_true", help="Enable all guardrails")
    
    args = parser.parse_args()
    
    # Create client
    client = MCPClient(
        llm_provider=args.provider,
        model=args.model,
        timeout=30.0,
        ssl_verify=False
    )
    
    # Add guardrails based on arguments
    if args.enable_all or args.enable_word_mask:
        word_guardrail = WordMaskGuardrail(
            name="sensitive_words",
            words_to_mask=["Texas", "California", "Flood", "password", "secret", "confidential", "private"],
            replacement="[REDACTED]"
        )
        client.add_guardrail(word_guardrail)
        print("✅ Word masking guardrail enabled")
    
    if args.enable_all or args.enable_pii:
        pii_guardrail = PIIGuardrail(name="pii_detection")
        client.add_guardrail(pii_guardrail)
        print("✅ PII detection guardrail enabled")
    
    if args.enable_all or args.enable_injection:
        injection_guardrail = InjectionGuardrail(name="injection_detection")
        client.add_guardrail(injection_guardrail)
        print("✅ Injection detection guardrail enabled")
    
    if args.enable_all or args.enable_response_block:
        response_block_guardrail = ResponseBlockGuardrail(
            name="response_blocking",
            blocked_words=["fire", "hack", "exploit", "vulnerability", "attack", "malware"],
            standardized_response="I apologize, but I cannot provide information about that topic for security reasons."
        )
        client.add_guardrail(response_block_guardrail)
        print("✅ Response blocking guardrail enabled")
    
    try:
        # Connect
        print(f"Connecting to {args.server}...")
        await client.connect(args.server, transport=args.transport)
        print("Connected!")
        
        # Show guardrails status
        print(f"\nGuardrails Status:")
        print(f"  Word Masking: {'✅' if (args.enable_all or args.enable_word_mask) else '❌'}")
        print(f"  PII Detection: {'✅' if (args.enable_all or args.enable_pii) else '❌'}")
        print(f"  Injection Detection: {'✅' if (args.enable_all or args.enable_injection) else '❌'}")
        print(f"  Response Blocking: {'✅' if (args.enable_all or args.enable_response_block) else '❌'}")
        
        # Chat loop
        print("\nChat started. Type 'exit' to quit, 'test' to run guardrail tests, 'status' to show guardrails.")
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() == 'exit':
                    break
                elif user_input.lower() == 'test':
                    await run_guardrail_tests(client)
                    continue
                elif user_input.lower() == 'status':
                    print(f"\nGuardrails Status:")
                    print(f"  Word Masking: {'✅' if (args.enable_all or args.enable_word_mask) else '❌'}")
                    print(f"  PII Detection: {'✅' if (args.enable_all or args.enable_pii) else '❌'}")
                    print(f"  Injection Detection: {'✅' if (args.enable_all or args.enable_injection) else '❌'}")
                    print(f"  Response Blocking: {'✅' if (args.enable_all or args.enable_response_block) else '❌'}")
                    continue
                
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


async def run_guardrail_tests(client):
    """Run example guardrail tests."""
    print("\n🧪 Running Guardrail Tests...")
    
    test_cases = [
        {
            "name": "Weather Guardrail Test",
            "input": "What is the weather in Texas? Any flood or fire warnings in California?",
            "description": "Tests redacting locations ('Texas', 'California', 'Flood') and blocking responses containing 'fire'."
        },
        {
            "name": "Word Masking Test",
            "input": "My password is 123456 and this is confidential information",
            "description": "Tests if sensitive words are masked"
        },
        {
            "name": "PII Detection Test", 
            "input": "Contact me at john.doe@example.com or call 123-456-7890",
            "description": "Tests if PII is detected and handled"
        },
        {
            "name": "Injection Detection Test",
            "input": "Here's a script: <script>alert('xss')</script>",
            "description": "Tests if injection attempts are detected"
        },
        {
            "name": "Response Blocking Test",
            "input": "How can I hack into a system?",
            "description": "Tests if blocked content triggers standardized response"
        },
        {
            "name": "Combined Test",
            "input": "My secret email is john.doe@example.com and I want to hack the system with <script>alert('xss')</script>",
            "description": "Tests multiple guardrails working together"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test['name']} ---")
        print(f"Description: {test['description']}")
        print(f"Input: {test['input']}")
        print("Processing...")
        
        try:
            response = await client.query(test['input'])
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n✅ Guardrail tests completed!")


if __name__ == "__main__":
    asyncio.run(main()) 