from __future__ import annotations
import subprocess
import os
import requests
import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="Git utilities")


@app.command()
@time_command
@log_command
def status():
    """Show git working tree status."""
    try:
        output = subprocess.check_output(["git", "status", "--short"], text=True)
    except Exception as exc:
        Console().print(f"git error: {exc}")
        raise typer.Exit(1)
    Console().print(output)


@app.command()
@time_command
@log_command
def diff(summary: bool = typer.Option(False, "--summary", help="Show diff summary")):
    """Show git diff or summary."""
    cmd = ["git", "diff"]
    if summary:
        cmd.append("--stat")
    try:
        output = subprocess.check_output(cmd, text=True)
    except Exception as exc:
        Console().print(f"git error: {exc}")
        raise typer.Exit(1)
    Console().print(output)


@app.command("pr-status")
@time_command
@log_command
def pr_status(repo: str = typer.Option(None, "--repo", help="owner/repo")):
    """Show recent pull requests for a repository."""
    if repo is None:
        try:
            origin = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True).strip()
            if origin.endswith(".git"):
                origin = origin[:-4]
            if origin.startswith("https://github.com/"):
                repo = origin[len("https://github.com/") :]
        except Exception:
            pass
    if not repo:
        Console().print("[red]Repository not specified[/red]")
        raise typer.Exit(1)
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
    for pr in resp.json():
        Console().print(f"#{pr['number']} {pr['title']}")


@app.command()
@time_command
@log_command
def changelog(last: int = typer.Option(5, "--last", help="Number of commits")):
    """Show recent commit messages."""
    try:
        output = subprocess.check_output(["git", "log", "-n", str(last), "--pretty=format:%h %s"], text=True)
    except Exception as exc:
        Console().print(f"git error: {exc}")
        raise typer.Exit(1)
    Console().print(output)
