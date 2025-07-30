from __future__ import annotations
import cmd
import shlex
import subprocess
import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="Interactive shell")

class ChatShell(cmd.Cmd):
    prompt = "chatops> "

    def default(self, line: str) -> None:
        args = shlex.split(line)
        if args:
            subprocess.call(["chatops", *args])

@time_command
@log_command
@app.command()
def start():
    """Start interactive shell."""
    Console().print("Starting shell. Type 'exit' to quit.")
    ChatShell().cmdloop()
