from __future__ import annotations
import subprocess
import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="Docker utilities")


@app.command()
@time_command
@log_command
def ps():
    """Show running Docker containers."""
    try:
        output = subprocess.check_output(["docker", "ps"], text=True)
    except Exception as exc:
        Console().print(f"docker error: {exc}")
        raise typer.Exit(1)
    Console().print(output)


@app.command()
@time_command
@log_command
def logs(container: str = typer.Argument(..., help="Container name")):
    """Show logs for a container."""
    try:
        output = subprocess.check_output(["docker", "logs", container, "--tail", "20"], text=True)
    except Exception as exc:
        Console().print(f"docker error: {exc}")
        raise typer.Exit(1)
    Console().print(output)


@app.command()
@time_command
@log_command
def build(path: str = typer.Option(".", "--path", help="Build context")):
    """Build a Docker image."""
    try:
        subprocess.check_call(["docker", "build", path])
    except Exception as exc:
        Console().print(f"docker error: {exc}")
        raise typer.Exit(1)


@app.command()
@time_command
@log_command
def scan(image: str = typer.Option(..., "--image", help="Image name")):
    """Simulate scanning a Docker image."""
    Console().print(f"Scanning image {image}... no issues found")
