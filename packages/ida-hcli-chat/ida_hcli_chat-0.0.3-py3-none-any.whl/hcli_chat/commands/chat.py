import os
import shutil
from textwrap import dedent
import logging
import threading
import rich_click as click
from agno.agent import Agent
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from hcli.lib.commands import async_command
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from hcli_chat.mcp.server import main as ida_server_main

memory = Memory()
console = Console()
history = InMemoryHistory()
session = PromptSession(history=history)
logger = logging.getLogger(__name__)

sse_thread = None
stop_server = threading.Event()

def run_sse_server() -> None:
    """Run the SSE server in a thread."""
    import sys

    # Mock sys.argv to pass the correct arguments to the server
    original_argv = sys.argv
    sys.argv = [
        "ida_pro_mcp.server",
        "--transport", "http://127.0.0.1:8744/sse"
    ]
    try:
        ida_server_main()
    except KeyboardInterrupt:
        pass
    finally:
        sys.argv = original_argv


def start_sse_server() -> None:
    """Start the SSE server in a background thread."""
    global sse_thread
    sse_thread = threading.Thread(target=run_sse_server, daemon=True)
    sse_thread.start()


def stop_sse_server() -> None:
    """Stop the SSE server thread."""
    global sse_thread
    if sse_thread and sse_thread.is_alive():
        stop_server.set()
        # Note: The server will stop when the main thread exits due to daemon=True


async def run_agent() -> None:
    """Run an interactive loop."""
    async with MCPTools(
            url="http://127.0.0.1:8744/sse", transport="sse") as mcp_tools:
        agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            add_history_to_messages=True,
            num_history_runs=3,
            show_tool_calls=True,

            tools=[mcp_tools],
            instructions=dedent("""\
                You are an experienced reverser. You know everything about assembly and compilers.
                - Be concise and focus on relevant information\
            """),
            markdown=True,
        )

        # Create a session once (can be reused for multiple prompts)
        while True:
            message = session.prompt(">> ", in_thread=True)

            if message in ("exit", "bye"):
                break

            try:
                await agent.aprint_response(message,
                                            console=console,
                                            stream=True,
                                            show_message=False,
                                            show_reasoning=True,
                                            show_full_reasoning=True)
            except Exception as e:
                logger.error(f"Error from OpenAI API: {e}")


@click.command
@async_command
async def chat(help="Chat with IDA") -> None:
    console.clear()
    welcome_message = r"""
      _____ _____                                                    
     |_   _|  __ \   /\                                              
       | | | |  | | /  \                                             
       | | | |  | |/ /\ \                                            
      _| |_| |__| / ____ \                                           
     |_____|_____/_/_ __\_\ _____  _____ _______       _   _ _______ 
         /\    / ____/ ____|_   _|/ ____|__   __|/\   | \ | |__   __|
        /  \  | (___| (___   | | | (___    | |  /  \  |  \| |  | |   
       / /\ \  \___ \\___ \  | |  \___ \   | | / /\ \ | . ` |  | |   
      / ____ \ ____) |___) |_| |_ ____) |  | |/ ____ \| |\  |  | |   
     /_/    \_\_____/_____/|_____|_____/   |_/_/    \_\_| \_|  |_|                                                                                                                                     
    """
    print(welcome_message)
    print(os.getenv("COLUMNS"))
    print(shutil.get_terminal_size())

    #console.print("Starting SSE server...")

    # Start the SSE server
    start_sse_server()

    try:
        console.print("Just type [bold]exit[/bold] to quit.")
        await run_agent()
    finally:
        # Clean up the SSE server
        #console.print("Shutting down SSE server...")
        stop_sse_server()
