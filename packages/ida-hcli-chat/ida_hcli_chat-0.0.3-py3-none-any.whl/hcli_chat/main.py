from __future__ import annotations

import rich_click as click
from rich.console import Console

from hcli_chat.commands import register

console = Console()

# Configure rich-click styling
click.rich_click.USE_RICH_MARKUP = True

@click.group()
@click.pass_context
def cli(_ctx):
    pass

# register subcommands
register(cli)

if __name__ == "__main__":
    cli()
