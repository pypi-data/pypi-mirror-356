import os
from types import ModuleType
import typer

import chatops.support as support

class DummyClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

openai_stub = ModuleType("openai")
openai_stub.OpenAI = DummyClient


def test_client_prompts_for_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(typer, "prompt", lambda text, hide_input=True: "testkey")
    monkeypatch.setattr(support, "openai", openai_stub)
    client = support._client()
    assert isinstance(client, DummyClient)
    assert client.api_key == "testkey"
    assert os.environ["OPENAI_API_KEY"] == "testkey"
