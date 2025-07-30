from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Security related commands")


@time_command
@log_command
@app.command("scan")
def scan(path: str):
    """Simulate static code scan for secrets."""
    Console().print(f"Scanning {path} ... no issues found")


@time_command
@log_command
@app.command("port-scan")
def port_scan(host: str):
    """Simulate open port scanning."""
    table = Table(title=f"Open ports on {host}")
    table.add_column("Port")
    table.add_row("22")
    table.add_row("443")
    Console().print(table)


@time_command
@log_command
@app.command("whoami")
def whoami():
    """Show current cloud identity."""
    Console().print("User: demo@example.com")
