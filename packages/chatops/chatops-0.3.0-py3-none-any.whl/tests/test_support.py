import os
from types import ModuleType
from typer.testing import CliRunner
import typer

import chatops.support as support
import chatops.openai_utils as openai_utils
from chatops import cli

class DummyClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

openai_stub = ModuleType("openai")
openai_stub.OpenAI = DummyClient


def test_client_prompts_for_api_key(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(typer, "prompt", lambda text, hide_input=True: "testkey")
    monkeypatch.setattr(openai_utils, "openai", openai_stub)
    monkeypatch.setattr(openai_utils.Path, "home", lambda: tmp_path)
    client = support._client()
    assert isinstance(client, DummyClient)
    assert client.api_key == "testkey"
    assert os.environ["OPENAI_API_KEY"] == "testkey"
    assert (tmp_path / ".openai_key").read_text() == "testkey"


def test_support_command(monkeypatch, tmp_path):
    """Support CLI should prompt for API key and run once provided."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # Stub OpenAI client returned by _client
    class DummyChat:
        def __init__(self):
            self.completions = self

        def create(self, *a, **k):  # noqa: D401 - simple stub
            class Resp:
                def __init__(self):
                    self.choices = [
                        type("C", (), {"message": type("M", (), {"content": "pong"})()})()
                    ]

            return Resp()

    class DummyClientFull(DummyClient):
        def __init__(self, api_key=None):
            super().__init__(api_key)
            self.chat = DummyChat()

    openai_stub.OpenAI = DummyClientFull
    monkeypatch.setattr(openai_utils, "openai", openai_stub)
    monkeypatch.setattr(openai_utils.Path, "home", lambda: tmp_path)

    # Provide API key when prompted
    monkeypatch.setattr(typer, "prompt", lambda text, hide_input=True: "testkey")

    # Replace Console and Markdown to automate interaction
    inputs = iter(["ping", "quit"])
    output = []

    class DummyConsole:
        def input(self, _=None):
            return next(inputs)

        def print(self, msg):
            output.append(str(msg))

    monkeypatch.setattr(support, "Console", DummyConsole)
    monkeypatch.setattr(support, "Markdown", lambda x: x)

    runner = CliRunner()
    result = runner.invoke(cli.app, ["support", "support"])

    assert result.exit_code == 0
    assert "Goodbye!" in output[-1]
    assert os.environ["OPENAI_API_KEY"] == "testkey"
