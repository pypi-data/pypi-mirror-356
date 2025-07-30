import asyncio
import os
import json
import sys
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from cerebromcp.memory.sqlite_memory import SQLiteMemory
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from cerebromcp.host_managed.internal_llm import InternalLLM

class LLMState(TypedDict):
    input: str
    output: str
    memory: SQLiteMemory
    next: str

async def openai_node(state: LLMState) -> LLMState:
    try:
        server_params = StdioServerParameters(
            command="python",
            args=["-u", "-m", "cerebromcp.servers.openai_server"],
            env={"PYTHONPATH": os.getcwd()}
        )
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                try:
                    await session.initialize()
                    response = await session.call_tool("openai_handler", {"prompt": state["input"]})
                    state["output"] = response.content[0].text if response.content else "No response"
                except Exception as e:
                    state["output"] = f"Error in OpenAI handler: {str(e)}"
    except Exception as e:
        state["output"] = f"Error connecting to OpenAI server: {str(e)}"
    return state

async def llama_node(state: LLMState) -> LLMState:
    try:
        server_params = StdioServerParameters(
            command="python",
            args=["-u", "-m", "cerebromcp.servers.llama_server"],
            env={"PYTHONPATH": os.getcwd()}
        )
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                try:
                    await session.initialize()
                    response = await session.call_tool("llama_handler", {"prompt": state["input"]})
                    state["output"] = response.content[0].text if response.content else "No response"
                except Exception as e:
                    state["output"] = f"Error in Llama handler: {str(e)}"
    except Exception as e:
        state["output"] = f"Error connecting to Llama server: {str(e)}"
    return state

async def rag_node(state: LLMState) -> LLMState:
    try:
        server_params = StdioServerParameters(
            command="python",
            args=["-u", "-m", "cerebromcp.servers.rag_mcp_server"],
            env={"PYTHONPATH": os.getcwd()}
        )
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                try:
                    await session.initialize()
                    response = await session.call_tool("rag_handler", {"prompt": state["input"]})
                    state["output"] = response.content[0].text if response.content else "No response"
                except Exception as e:
                    state["output"] = f"Error in RAG handler: {str(e)}"
    except Exception as e:
        state["output"] = f"Error connecting to RAG server: {str(e)}"
    return state

async def crewai_node(state: LLMState) -> LLMState:
    try:
        server_params = StdioServerParameters(
            command="python",
            args=["-u", "-m", "cerebromcp.servers.crewai_server"],
            env={"PYTHONPATH": os.getcwd()}
        )
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                try:
                    await session.initialize()
                    response = await session.call_tool("crewai_handler", {"prompt": state["input"]})
                    state["output"] = response.content[0].text if response.content else "No response"
                except Exception as e:
                    state["output"] = f"Error in CrewAI handler: {str(e)}"
    except Exception as e:
        state["output"] = f"Error connecting to CrewAI server: {str(e)}"
    return state

async def persistent_node(state: LLMState) -> LLMState:
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8765)
        try:
            # Read initialization message
            length_bytes = await reader.read(4)
            if not length_bytes:
                raise ConnectionError("Connection closed by server")
            length = int.from_bytes(length_bytes, 'big')
            print(f"Received init message length: {length}", file=sys.stderr)
            
            init_msg = await reader.read(length)
            if not init_msg:
                raise ConnectionError("Connection closed by server")
            init_str = init_msg.decode('utf-8')
            print(f"Received init message: {init_str}", file=sys.stderr)
            
            try:
                init_response = json.loads(init_str)
                if not isinstance(init_response, dict) or "jsonrpc" not in init_response:
                    raise ValueError("Invalid initialization message format")
            except json.JSONDecodeError as e:
                print(f"JSON decode error in init message: {str(e)}", file=sys.stderr)
                raise ValueError(f"Invalid JSON in initialization message: {str(e)}")
            
            # Send tool call
            call_msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "callTool",
                "params": {
                    "name": "echo_handler",
                    "arguments": {"prompt": state["input"]}
                }
            }
            call_str = json.dumps(call_msg)
            print(f"Sending call message: {call_str}", file=sys.stderr)
            call_bytes = call_str.encode('utf-8')
            writer.write(len(call_bytes).to_bytes(4, 'big'))
            writer.write(call_bytes)
            await writer.drain()
            
            # Read response
            length_bytes = await reader.read(4)
            length = int.from_bytes(length_bytes, 'big')
            print(f"Received response length: {length}", file=sys.stderr)
            
            response_bytes = await reader.read(length)
            response_str = response_bytes.decode('utf-8')
            print(f"Received response: {response_str}", file=sys.stderr)
            
            try:
                response = json.loads(response_str)
                if "result" in response and "content" in response["result"]:
                    state["output"] = response["result"]["content"][0]["text"]
                else:
                    state["output"] = "No response or invalid response format"
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}", file=sys.stderr)
                state["output"] = f"Error parsing response: {str(e)}"
                
        except Exception as e:
            print(f"Error in persistent handler: {str(e)}", file=sys.stderr)
            state["output"] = f"Error in persistent handler: {str(e)}"
        finally:
            writer.close()
            await writer.wait_closed()
    except Exception as e:
        print(f"Error connecting to persistent server: {str(e)}", file=sys.stderr)
        state["output"] = f"Error connecting to persistent server: {str(e)}"
    return state

async def internal_node(state: LLMState) -> LLMState:
    try:
        llm = InternalLLM()
        response = await llm.generate(state["input"])
        state["output"] = response
    except Exception as e:
        state["output"] = f"Error in Internal LLM handler: {str(e)}"
    return state

def route_node(state: LLMState) -> LLMState:
    # Simple routing based on input content
    input_text = state["input"].lower()
    if "openai" in input_text:
        state["next"] = "openai"
    elif "llama" in input_text:
        state["next"] = "llama"
    elif "rag" in input_text or "search" in input_text:
        state["next"] = "rag"
    elif "crew" in input_text or "team" in input_text:
        state["next"] = "crewai"
    elif "persistent" in input_text:
        state["next"] = "persistent"
    else:
        state["next"] = "internal"
    return state

async def main():
    # Initialize memory
    memory = SQLiteMemory()
    await memory.initialize()

    # Create workflow
    workflow = StateGraph(LLMState)

    # Add nodes
    workflow.add_node("route", route_node)
    workflow.add_node("internal", internal_node)
    workflow.add_node("openai", openai_node)
    workflow.add_node("llama", llama_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("crewai", crewai_node)
    workflow.add_node("persistent", persistent_node)

    # Add edges
    workflow.add_conditional_edges(
        "route",
        lambda x: x["next"],
        {
            "internal": "internal",
            "openai": "openai",
            "llama": "llama",
            "rag": "rag",
            "crewai": "crewai",
            "persistent": "persistent"
        }
    )

    # Add edges to END
    workflow.add_edge("internal", END)
    workflow.add_edge("openai", END)
    workflow.add_edge("llama", END)
    workflow.add_edge("rag", END)
    workflow.add_edge("crewai", END)
    workflow.add_edge("persistent", END)

    # Set entry point
    workflow.set_entry_point("route")

    # Compile workflow
    app = workflow.compile()

    # Main loop
    while True:
        try:
            user_input = input("\nEnter your prompt (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break

            # Create initial state
            state = {
                "input": user_input,
                "output": "",
                "memory": memory
            }

            # Run workflow
            result = await app.ainvoke(state)
            print("\nResponse:", result["output"])

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

    # Cleanup
    await memory.close()

if __name__ == "__main__":
    asyncio.run(main())