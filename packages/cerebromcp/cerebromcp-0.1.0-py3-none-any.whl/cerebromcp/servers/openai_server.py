import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio
import sys
import json

load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create server instance
server = Server("openai-server")

@server.call_tool()
async def openai_handler(name: str, arguments: dict) -> types.CallToolResult:
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return types.CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Error: OPENAI_API_KEY not found in environment variables"
                }]
            )
        
        prompt = arguments.get("prompt", "")
        if not prompt:
            return types.CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Error: No prompt provided"
                }]
            )
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return types.CallToolResult(
            content=[{
                "type": "text",
                "text": response.choices[0].message.content
            }]
        )
    except Exception as e:
        error_msg = f"Error in OpenAI server: {str(e)}"
        print(error_msg, file=sys.stderr)
        return types.CallToolResult(
            content=[{
                "type": "text",
                "text": error_msg
            }]
        )

async def run():
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="openai-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        print(f"Server error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1) 