from __future__ import annotations
import subprocess
import typer
from rich.console import Console
from .utils import log_command, time_command
from . import env as env_mod

app = typer.Typer(help="Docker utilities")


def _require(ctx: typer.Context) -> None:
    env_cfg = env_mod.get_env(ctx.obj.get("env_override"))
    if not env_cfg or env_cfg.get("provider") != "docker":
        Console().print("[red]Docker environment required[/red]")
        raise typer.Exit(1)


@app.command()
@time_command
@log_command
def ps(ctx: typer.Context):
    _require(ctx)
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
def logs(ctx: typer.Context, container: str = typer.Argument(..., help="Container name")):
    """Show logs for a container."""
    _require(ctx)
    try:
        output = subprocess.check_output(["docker", "logs", container, "--tail", "20"], text=True)
    except Exception as exc:
        Console().print(f"docker error: {exc}")
        raise typer.Exit(1)
    Console().print(output)


@app.command()
@time_command
@log_command
def build(
    ctx: typer.Context, path: str = typer.Option(".", "--path", help="Build context")
):
    """Build a Docker image."""
    _require(ctx)
    try:
        subprocess.check_call(["docker", "build", path])
    except Exception as exc:
        Console().print(f"docker error: {exc}")
        raise typer.Exit(1)


@app.command()
@time_command
@log_command
def scan(
    ctx: typer.Context, image: str = typer.Option(..., "--image", help="Image name")
):
    """Simulate scanning a Docker image."""
    _require(ctx)
    Console().print(f"Scanning image {image}... no issues found")

