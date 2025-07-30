from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="IAM related commands")


@time_command
@log_command
@app.command("list-admins")
def list_admins():
    """Print fake IAM users with admin roles."""
    table = Table(title="Admins")
    table.add_column("User")
    for user in ["alice", "bob"]:
        table.add_row(user)
    Console().print(table)


@time_command
@log_command
@app.command("check-expired")
def check_expired():
    """Simulate scan for expired credentials."""
    Console().print("No expired credentials found")


@time_command
@log_command
@app.command()
def audit():
    """Show IAM misconfigurations."""
    table = Table(title="IAM Audit")
    table.add_column("Issue")
    table.add_row("User with wildcard policy")
    Console().print(table)
