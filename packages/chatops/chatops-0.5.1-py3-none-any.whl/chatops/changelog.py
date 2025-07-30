from __future__ import annotations
import subprocess
import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="Changelog commands")

@time_command
@log_command
@app.command("latest")
def latest():
    """Show summary of recent commits."""
    try:
        output = subprocess.check_output(["git", "log", "-n", "5", "--pretty=format:%h %s"], text=True)
    except Exception as exc:
        Console().print(f"git error: {exc}")
        raise typer.Exit(1)
    Console().print(output)
