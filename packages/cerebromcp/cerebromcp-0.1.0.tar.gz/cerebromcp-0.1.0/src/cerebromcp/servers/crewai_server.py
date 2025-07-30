import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
import asyncio
import sys
import json

load_dotenv()

# Create server instance
server = Server("crewai-server")

@server.call_tool()
async def crewai_handler(name: str, arguments: dict) -> types.CallToolResult:
    try:
        prompt = arguments.get("prompt", "")
        if not prompt:
            return types.CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Error: No prompt provided"
                }]
            )
            
        researcher = Agent(
            name="Researcher",
            goal="Find useful knowledge",
            backstory="A domain expert in research and analysis",
            verbose=True
        )
        
        writer = Agent(
            name="Writer",
            goal="Summarize information clearly",
            backstory="A technical writer with expertise in making complex topics accessible",
            verbose=True
        )

        research_task = Task(
            description=f"Research and analyze: {prompt}",
            agent=researcher
        )

        writing_task = Task(
            description="Summarize the research findings in a clear and concise way",
            agent=writer
        )

        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            verbose=True
        )

        result = crew.kickoff()
        
        return types.CallToolResult(
            content=[{
                "type": "text",
                "text": result
            }]
        )
    except Exception as e:
        error_msg = f"Error in CrewAI server: {str(e)}"
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
                    server_name="crewai-server",
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