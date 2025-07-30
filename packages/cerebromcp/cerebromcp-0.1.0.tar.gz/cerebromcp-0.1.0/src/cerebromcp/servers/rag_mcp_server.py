import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
import asyncio
import sys
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Create server instance
server = Server("rag-server")

@server.call_tool()
async def rag_handler(name: str, arguments: dict) -> types.CallToolResult:
    try:
        prompt = arguments.get("prompt", "")
        if not prompt:
            return types.CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Error: No prompt provided"
                }]
            )
            
        # Implement RAG functionality here
        # This is a placeholder implementation
        response = f"RAG response to: {prompt}"
        
        return types.CallToolResult(
            content=[{
                "type": "text",
                "text": response
            }]
        )
    except Exception as e:
        error_msg = f"Error in RAG server: {str(e)}"
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
                    server_name="rag-server",
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