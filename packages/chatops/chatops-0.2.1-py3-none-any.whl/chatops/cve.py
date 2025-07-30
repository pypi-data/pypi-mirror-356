from __future__ import annotations
import requests
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="CVE related commands")


@time_command
@log_command
@app.command()
def latest():
    """Fetch recent CVEs from cve.circl.lu."""
    try:
        resp = requests.get("https://cve.circl.lu/api/last", timeout=10)
    except Exception as exc:
        Console().print(f"Request failed: {exc}")
        raise typer.Exit(1)
    if resp.status_code != 200:
        Console().print(f"Failed to fetch CVEs: {resp.status_code}")
        raise typer.Exit(1)
    data = resp.json()[:5]
    table = Table(title="Latest CVEs")
    table.add_column("id")
    table.add_column("summary")
    for item in data:
        table.add_row(item.get("id", ""), item.get("summary", ""))
    Console().print(table)


@time_command
@log_command
@app.command()
def search(keyword: str = typer.Option(..., "--keyword")):
    """Simulate filtering CVEs."""
    table = Table(title=f"CVEs matching {keyword}")
    table.add_column("id")
    for i in range(3):
        table.add_row(f"CVE-2024-000{i}")
    Console().print(table)
