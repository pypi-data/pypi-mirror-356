import asyncio
import json
import sys
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Create server instance
server = Server("persistent-server")

@server.call_tool()
async def echo_handler(name: str, arguments: dict) -> types.CallToolResult:
    try:
        prompt = arguments.get("prompt", "")
        if not prompt:
            return types.CallToolResult(
                content=[types.TextContent(type="text", text="Error: No prompt provided")]
            )
        response = f"Echo: {prompt}"
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=response)]
        )
    except Exception as e:
        error_msg = f"Error in persistent server: {str(e)}"
        print(error_msg, file=sys.stderr)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=error_msg)]
        )

class MCPStreamReader:
    def __init__(self, reader):
        self.reader = reader
        self.buffer = b""

    async def read(self, n):
        while len(self.buffer) < n:
            chunk = await self.reader.read(1024)
            if not chunk:
                raise EOFError("Connection closed")
            self.buffer += chunk
        data = self.buffer[:n]
        self.buffer = self.buffer[n:]
        return data

async def handle_client(reader, writer):
    try:
        mcp_reader = MCPStreamReader(reader)
        
        # Send initialization message
        init_msg = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "serverName": "persistent-server",
                "serverVersion": "0.1.0",
                "capabilities": {
                    "notificationOptions": {},
                    "experimentalCapabilities": {}
                }
            }
        }
        print("Sending initialization message...", file=sys.stderr)
        init_str = json.dumps(init_msg, ensure_ascii=False)
        init_bytes = init_str.encode('utf-8')
        writer.write(len(init_bytes).to_bytes(4, 'big'))
        writer.write(init_bytes)
        await writer.drain()
        
        # Handle client messages
        while True:
            try:
                # Read message length (4 bytes)
                length_bytes = await mcp_reader.read(4)
                length = int.from_bytes(length_bytes, 'big')
                print(f"Received message length: {length}", file=sys.stderr)
                
                # Read message content
                content = await mcp_reader.read(length)
                message_str = content.decode('utf-8')
                print(f"Received message: {message_str}", file=sys.stderr)
                message = json.loads(message_str)
                
                # Process message
                if message.get("method") == "callTool":
                    print(f"Processing tool call: {message}", file=sys.stderr)
                    result = await echo_handler(
                        message["params"]["name"],
                        message["params"]["arguments"]
                    )
                    response = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result.content[0].text
                                }
                            ]
                        }
                    }
                    print(f"Sending response: {response}", file=sys.stderr)
                    response_str = json.dumps(response, ensure_ascii=False)
                    response_bytes = response_str.encode('utf-8')
                    writer.write(len(response_bytes).to_bytes(4, 'big'))
                    writer.write(response_bytes)
                    await writer.drain()
                
            except EOFError:
                print("Client disconnected", file=sys.stderr)
                break
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}", file=sys.stderr)
                break
            except Exception as e:
                print(f"Error processing message: {str(e)}", file=sys.stderr)
                break
                
    except Exception as e:
        print(f"Client error: {str(e)}", file=sys.stderr)
    finally:
        writer.close()
        await writer.wait_closed()

async def run():
    try:
        server = await asyncio.start_server(
            handle_client,
            '127.0.0.1',
            8765
        )
        print("Persistent MCP server running on 127.0.0.1:8765", file=sys.stderr)
        
        async with server:
            await server.serve_forever()
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