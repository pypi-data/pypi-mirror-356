from __future__ import annotations
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None


def ensure_api_key(console: Optional[Console] = None) -> str:
    """Return a valid OpenAI API key, prompting the user if needed."""
    if openai is None:
        raise RuntimeError("openai package not installed")

    if console is None:
        console = Console()

    api_key = os.environ.get("OPENAI_API_KEY")
    key_file = Path.home() / ".openai_key"

    if not api_key and key_file.exists():
        try:
            stored = key_file.read_text().strip()
            if stored:
                api_key = stored
                os.environ["OPENAI_API_KEY"] = api_key
                console.print(f"[green]Loaded API key from {key_file}[/green]")
        except Exception:  # pragma: no cover - ignore read errors
            pass

    if not api_key:
        console.print("[yellow]OPENAI_API_KEY not set[/yellow]")
        api_key = typer.prompt("Enter your OpenAI API key", hide_input=True)
        if not api_key:
            console.print("[red]No API key provided[/red]")
            raise typer.Exit(1)
        os.environ["OPENAI_API_KEY"] = api_key
        try:
            key_file.write_text(api_key)
            console.print(f"[green]Saved API key to {key_file}[/green]")
        except Exception:  # pragma: no cover - ignore write errors
            console.print(f"[yellow]Could not write {key_file}[/yellow]")

    openai.api_key = api_key
    return api_key


def openai_client(console: Optional[Console] = None) -> "openai.OpenAI":
    """Return an OpenAI client with a valid API key."""
    api_key = ensure_api_key(console)
    return openai.OpenAI(api_key=api_key)
