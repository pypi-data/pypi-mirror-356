from textwrap import dedent
import logging
import rich_click as click
from agno.agent import Agent
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from hcli.lib.commands import async_command
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console

memory = Memory()
console = Console()
history = InMemoryHistory()
session = PromptSession(history=history)
logger = logging.getLogger(__name__)


async def run_agent() -> None:
    """Run an interactive loop."""
    async with MCPTools(
            "/Users/plosson/.idapro/venv/bin/python3 /Users/plosson/.idapro/venv/lib/python3.13/site-packages/ida_pro_mcp/server.py") as mcp_tools:
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
                                            stream=True,
                                            show_message=False,
                                            show_reasoning=True,
                                            show_full_reasoning=True)
            except Exception as e:
                logger.error(f"Error from OpenAI API: {e}")


@click.command
@async_command
async def chat() -> None:
    console.clear()
    console.print("Just type [bold]exit[/bold] to quit.")
    await run_agent()
