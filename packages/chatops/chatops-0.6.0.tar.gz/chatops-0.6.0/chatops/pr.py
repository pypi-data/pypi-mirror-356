from __future__ import annotations
import os
import requests
import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="GitHub PR utilities")

@time_command
@log_command
@app.command("status")
def status(repo: str = typer.Argument(..., help="owner/repo")):
    """Show recent pull requests."""
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"https://api.github.com/repos/{repo}/pulls?state=open&per_page=5"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except Exception as exc:
        Console().print(f"Request failed: {exc}")
        raise typer.Exit(1)
    if resp.status_code != 200:
        Console().print(f"Failed to fetch PRs: {resp.status_code}")
        raise typer.Exit(1)
    data = resp.json()
    console = Console()
    for pr in data:
        console.print(f"#{pr['number']} {pr['title']}")
