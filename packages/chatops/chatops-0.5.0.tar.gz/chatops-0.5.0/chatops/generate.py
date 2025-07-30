from __future__ import annotations
import subprocess
from pathlib import Path
import typer
from rich.console import Console
from .openai_utils import openai_client
from .utils import log_command, time_command

try:
    import openai
except Exception:  # pragma: no cover
    openai = None

app = typer.Typer(help="Infrastructure and CI/CD generation")


@time_command
@log_command
@app.command()
def terraform(
    resource: str = typer.Argument(..., help="Resource name"),
    secure: bool = typer.Option(False, "--secure", help="Enable security best practices"),
    versioning: bool = typer.Option(False, "--versioning", help="Enable state versioning"),
    apply: bool = typer.Option(False, "--apply", help="Apply with Terraform"),
):
    """Generate Terraform configuration."""
    console = Console()
    try:
        client = openai_client(console)
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)

    prompt = f"Generate Terraform config for {resource}."
    if secure:
        prompt += " Use secure defaults."
    if versioning:
        prompt += " Enable versioning where applicable."

    resp = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}], stream=True
    )
    parts: list[str] = []
    if hasattr(resp, "__iter__"):
        for chunk in resp:
            delta = chunk.choices[0].delta.content
            if delta:
                console.print(delta, end="")
                parts.append(delta)
        console.print()
    content = "".join(parts)

    path = Path("generated.tf")
    path.write_text(content)
    console.print(f"[green]Wrote {path}")

    if apply:
        console.print("[cyan]Applying configuration...[/cyan]")
        subprocess.call(["terraform", "init"])
        subprocess.call(["terraform", "apply", "-auto-approve"])


@time_command
@log_command
@app.command()
def dockerfile(apply: bool = typer.Option(False, "--apply", help="Build Docker image")):
    """Generate a Dockerfile using OpenAI."""
    console = Console()
    try:
        client = openai_client(console)
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)

    prompt = "Generate a secure Dockerfile for a Python web app"
    resp = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}], stream=True
    )
    parts: list[str] = []
    if hasattr(resp, "__iter__"):
        for chunk in resp:
            delta = chunk.choices[0].delta.content
            if delta:
                console.print(delta, end="")
                parts.append(delta)
        console.print()
    content = "".join(parts)
    path = Path("Dockerfile")
    path.write_text(content)
    console.print("[green]Wrote Dockerfile")
    if apply:
        subprocess.call(["docker", "build", "-t", "generated:latest", "."])


@time_command
@log_command
@app.command(name="github-actions")
def github_actions(apply: bool = typer.Option(False, "--apply", help="Commit workflow")):
    """Generate GitHub Actions workflow."""
    console = Console()
    try:
        client = openai_client(console)
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)

    prompt = "Generate a CI/CD GitHub Actions workflow for a Python project"
    resp = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}], stream=True
    )
    parts: list[str] = []
    if hasattr(resp, "__iter__"):
        for chunk in resp:
            delta = chunk.choices[0].delta.content
            if delta:
                console.print(delta, end="")
                parts.append(delta)
        console.print()
    content = "".join(parts)
    path = Path(".github/workflows/ci.yml")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    console.print(f"[green]Wrote {path}")
    if apply:
        subprocess.call(["git", "add", str(path)])
        subprocess.call(["git", "commit", "-m", "Add generated workflow"])

