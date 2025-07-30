from __future__ import annotations
import os
import typer
from rich.console import Console
from rich.markdown import Markdown
from .utils import log_command, time_command

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None

app = typer.Typer(help="Interactive support assistant")


def _client() -> 'openai.OpenAI':
    if openai is None:
        raise RuntimeError("openai package not installed")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Prompt the user for an API key if not already set
        api_key = typer.prompt(
            "Enter your OpenAI API key", hide_input=True
        )
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not provided")
        os.environ["OPENAI_API_KEY"] = api_key
    return openai.OpenAI(api_key=api_key)


@time_command
@log_command
@app.command()
def support():
    """Launch an interactive DevOps assistant."""
    console = Console()
    try:
        client = _client()
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)

    messages = [
        {"role": "system", "content": "You are a helpful DevOps and cloud assistant"}
    ]

    while True:
        try:
            user_input = console.input("[bold blue]support> [/bold blue]")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        messages.append({"role": "user", "content": user_input})
        try:
            resp = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.2,
            )
            reply = resp.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            console.print(Markdown(reply))
        except Exception as exc:
            console.print(f"[red]Error: {exc}[/red]")
    console.print("[green]Goodbye![/green]")
