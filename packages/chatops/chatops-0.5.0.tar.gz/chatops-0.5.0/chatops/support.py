from __future__ import annotations
import typer
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path
from datetime import datetime
from .utils import log_command, time_command
from .openai_utils import openai_client
from . import history

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None

app = typer.Typer(help="Interactive support assistant")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Run interactive assistant when invoked directly."""
    if ctx.invoked_subcommand is None:
        support()


def _client(console: Console | None = None) -> 'openai.OpenAI':
    """Return an OpenAI client after ensuring an API key is available."""
    return openai_client(console)


@time_command
@log_command
def support(share: bool = typer.Option(False, "--share", help="Export session as Markdown")) -> None:
    """Launch an interactive DevOps assistant."""
    console = Console()
    try:
        client = _client(console)
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)

    transcript: list[str] = []
    messages = [
        {"role": "system", "content": "You are a helpful DevOps and cloud assistant"}
    ]

    for name in ["Dockerfile", "main.tf", ".env", "pyproject.toml"]:
        path = Path.cwd() / name
        if path.exists():
            try:
                content = path.read_text()[:1000]
                messages.append({"role": "system", "content": f"{name} contents:\n{content}"})
            except Exception:
                pass

    hist = history.recent(6)
    for item in hist:
        if item.get("role") in {"user", "assistant"}:
            messages.append({"role": item["role"], "content": item["content"]})

    while True:
        try:
            user_input = console.input("[bold blue]support> [/bold blue]")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        messages.append({"role": "user", "content": user_input})
        transcript.append(f"**User:** {user_input}")
        history.add_entry({"timestamp": datetime.utcnow().isoformat(), "role": "user", "content": user_input})
        try:
            resp = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.2,
                stream=True,
            )
            parts: list[str] = []
            if hasattr(resp, "__iter__"):
                for chunk in resp:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        console.print(delta, end="")
                        parts.append(delta)
                console.print()
                reply = "".join(parts)
            else:
                reply = resp.choices[0].message.content
                console.print(Markdown(reply))
            messages.append({"role": "assistant", "content": reply})
            transcript.append(f"**Assistant:** {reply}")
            history.add_entry({"timestamp": datetime.utcnow().isoformat(), "role": "assistant", "content": reply})
        except Exception as exc:
            console.print(f"[red]Error: {exc}[/red]")
    if share:
        md = "\n".join(transcript)
        Path("support_session.md").write_text(md)
        console.print("[cyan]Session saved to support_session.md[/cyan]")
    console.print("[green]Goodbye![/green]")

