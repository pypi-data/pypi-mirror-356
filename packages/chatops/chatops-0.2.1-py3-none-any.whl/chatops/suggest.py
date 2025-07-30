import os
from typing import List, Tuple

import numpy as np
import openai


# Known CLI commands and a short description for embedding purposes
_COMMANDS: List[Tuple[str, str]] = [
    ("deploy deploy APP ENV", "Deploy the given app to the specified environment"),
    ("deploy status", "Show deployment status"),
    ("deploy rollback APP ENV", "Rollback to the last successful deployment"),
    ("logs show", "Show recent log entries"),
    (
        "cost report azure SUBSCRIPTION_ID",
        "Show Azure cost by service for the current month",
    ),
    ("incident list", "List current incidents"),
    ("security scan", "Run security scan"),
]

# Cache for command embeddings
_COMMAND_EMBEDDINGS: List[Tuple[str, np.ndarray]] | None = None


def _get_client() -> openai.OpenAI:
    """Return an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    return openai.OpenAI(api_key=api_key)


def _embed(text: str, client: openai.OpenAI) -> np.ndarray:
    """Return the embedding vector for the given text."""
    response = client.embeddings.create(model="text-embedding-3-small", input=[text])
    return np.array(response.data[0].embedding, dtype=float)


def _load_command_embeddings(client: openai.OpenAI) -> List[Tuple[str, np.ndarray]]:
    """Compute and cache embeddings for known commands."""
    global _COMMAND_EMBEDDINGS
    if _COMMAND_EMBEDDINGS is None:
        _COMMAND_EMBEDDINGS = []
        for cmd, desc in _COMMANDS:
            _COMMAND_EMBEDDINGS.append((cmd, _embed(desc, client)))
    return _COMMAND_EMBEDDINGS


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def suggest_command(user_query: str) -> str:
    """Return the CLI command that best matches the plain English query.

    Parameters
    ----------
    user_query: str
        A natural language request like ``"restart app on prod"``.

    Returns
    -------
    str
        The closest matching CLI command string.
    """
    client = _get_client()
    query_emb = _embed(user_query, client)
    commands = _load_command_embeddings(client)

    best_cmd = max(commands, key=lambda pair: _cosine_similarity(query_emb, pair[1]))
    return best_cmd[0]

import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="AI powered helpers")


@time_command
@log_command
@app.command()
def suggest(prompt: str):
    """Suggest best ChatOps command."""
    try:
        cmd = suggest_command(prompt)
    except Exception as exc:
        Console().print(f"Error: {exc}")
        raise typer.Exit(1)
    Console().print(cmd)


@time_command
@log_command
@app.command()
def explain(text: str):
    """Use OpenAI to explain an error message."""
    try:
        client = _get_client()
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])
        Console().print(resp.choices[0].message.content)
    except Exception as exc:
        Console().print(f"OpenAI error: {exc}")
        raise typer.Exit(1)
