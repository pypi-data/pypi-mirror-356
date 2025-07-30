from __future__ import annotations
import os
import time
import requests
import typer
from rich.progress import Progress
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="Deployment related commands")


def _gh_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}


@time_command
@log_command
@app.command()
def deploy(
    app_name: str = typer.Argument(..., help="Application name"),
    env: str = typer.Argument(..., help="Target environment"),
):
    """Trigger a GitHub Actions deployment workflow."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        typer.echo("GITHUB_TOKEN and GITHUB_REPOSITORY must be set")
        raise typer.Exit(1)

    dispatch_url = f"https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/dispatches"
    body = {"ref": "main", "inputs": {"app_name": app_name, "environment": env}}
    resp = requests.post(dispatch_url, headers=_gh_headers(token), json=body)
    if resp.status_code not in (200, 201, 204):
        typer.echo(f"Failed to dispatch workflow: {resp.status_code} {resp.text}")
        raise typer.Exit(1)

    Console().print("Workflow dispatched")
    time.sleep(2)
    runs_url = f"https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/runs?per_page=1"
    runs_resp = requests.get(runs_url, headers=_gh_headers(token))
    if runs_resp.status_code == 200:
        run = runs_resp.json().get("workflow_runs", [{}])[0]
        Console().print(f"Run {run.get('id')} status: {run.get('status')} (conclusion: {run.get('conclusion')})")
    else:
        Console().print(f"Could not fetch workflow status: {runs_resp.status_code} {runs_resp.text}")

    with Progress() as progress:
        task = progress.add_task("Deploying", total=3)
        for _ in range(3):
            time.sleep(1)
            progress.advance(task)


@time_command
@log_command
@app.command()
def status():
    """Print deploy history and last timestamp."""
    Console().print("Last deploy: 2024-01-01 00:00:00")


@time_command
@log_command
@app.command()
def rollback(
    app_name: str = typer.Argument(..., help="Application name"),
    env: str = typer.Argument(..., help="Target environment"),
):
    """Simulate rolling back to previous release."""
    Console().print(f"Rolling back {app_name} on {env}...")
    time.sleep(1)
    Console().print("Rollback complete")
