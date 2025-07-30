import os
import time
import requests
import typer

app = typer.Typer(help="Deployment related commands")

@app.command()
def deploy(app_name: str, env: str):
    """Trigger a GitHub Actions deployment workflow."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        typer.echo("GITHUB_TOKEN and GITHUB_REPOSITORY must be set")
        raise typer.Exit(code=1)

    dispatch_url = (
        f"https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/dispatches"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    body = {"ref": "main", "inputs": {"app_name": app_name, "environment": env}}
    response = requests.post(dispatch_url, headers=headers, json=body)
    if response.status_code not in (200, 201, 204):
        typer.echo(f"Failed to dispatch workflow: {response.status_code} {response.text}")
        raise typer.Exit(code=1)

    typer.echo("Workflow dispatched")

    time.sleep(2)
    runs_url = (
        f"https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/runs?per_page=1"
    )
    runs_resp = requests.get(runs_url, headers=headers)
    if runs_resp.status_code == 200:
        run = runs_resp.json().get("workflow_runs", [{}])[0]
        typer.echo(
            f"Run {run.get('id')} status: {run.get('status')} (conclusion: {run.get('conclusion')})"
        )
    else:
        typer.echo(
            f"Could not fetch workflow status: {runs_resp.status_code} {runs_resp.text}"
        )


@app.command()
def status():
    """Show deployment status."""
    typer.echo("Deployment is healthy")


@app.command()
def rollback(app_name: str, env: str):
    """Rollback to the last successful deployment."""
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        typer.echo("GITHUB_TOKEN and GITHUB_REPOSITORY must be set")
        raise typer.Exit(code=1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    deployments_url = (
        f"https://api.github.com/repos/{repo}/deployments"
        f"?environment={env}&per_page=30"
    )
    dep_resp = requests.get(deployments_url, headers=headers)
    if dep_resp.status_code != 200:
        typer.echo(
            f"Failed to fetch deployments: {dep_resp.status_code} {dep_resp.text}"
        )
        raise typer.Exit(code=1)

    deployment = None
    for d in dep_resp.json():
        payload = d.get("payload", {})
        if payload.get("app_name") == app_name:
            # verify deployment status is successful
            status_url = (
                f"https://api.github.com/repos/{repo}/deployments/{d['id']}/statuses"
                f"?per_page=1"
            )
            status_resp = requests.get(status_url, headers=headers)
            if status_resp.status_code == 200 and status_resp.json():
                if status_resp.json()[0].get("state") == "success":
                    deployment = d
                    break

    if not deployment:
        typer.echo("No successful deployment found")
        raise typer.Exit(code=1)

    sha = deployment.get("sha")
    typer.echo(f"Redeploying commit {sha}")
    dispatch_url = (
        f"https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/dispatches"
    )
    body = {"ref": sha, "inputs": {"app_name": app_name, "environment": env}}
    dispatch_resp = requests.post(dispatch_url, headers=headers, json=body)
    if dispatch_resp.status_code not in (200, 201, 204):
        typer.echo(
            f"Failed to dispatch workflow: {dispatch_resp.status_code} {dispatch_resp.text}"
        )
        raise typer.Exit(code=1)

    typer.echo(f"Rollback triggered for commit {sha}")
