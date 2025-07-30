from __future__ import annotations
import typer
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Security related commands")


@time_command
@log_command
@app.command("scan")
def scan(path: str = typer.Argument(..., help="Path to scan")):
    """Simple regex based secret scan."""
    matches = []
    try:
        text = Path(path).read_text()
        patterns = [r"AKIA[0-9A-Z]{16}", r"SECRET_KEY"]
        for pat in patterns:
            for m in re.findall(pat, text):
                matches.append(m)
    except Exception:
        pass
    if matches:
        Console().print(f"[red]Potential secrets found: {matches}[/red]")
    else:
        Console().print(f"Scanning {path} ... no issues found")


@time_command
@log_command
@app.command("port-scan")
def port_scan(host: str = typer.Argument(..., help="Host to scan")):
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


@time_command
@log_command
@app.command("docker-scan")
def docker_scan(image: str = typer.Argument(..., help="Docker image")):
    """Simulate Docker image vulnerability scan."""
    Console().print(f"Scanning Docker image {image} ... no vulnerabilities found")
