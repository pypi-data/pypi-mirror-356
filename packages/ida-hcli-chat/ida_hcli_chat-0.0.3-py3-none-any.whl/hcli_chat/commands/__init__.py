import rich_click as click

def register(cli: click.Group):
    from .chat import chat
    cli.add_command(chat)
