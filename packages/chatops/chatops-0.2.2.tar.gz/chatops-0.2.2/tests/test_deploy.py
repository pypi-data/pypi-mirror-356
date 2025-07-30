import sys
from types import ModuleType
import time
from typer.testing import CliRunner
import requests
import pytest

# Provide dummy modules for optional dependencies used during import
sys.modules.setdefault("boto3", ModuleType("boto3"))
sys.modules.setdefault("azure", ModuleType("azure"))

azure_identity = ModuleType("azure.identity")
azure_identity.AzureCliCredential = object
sys.modules.setdefault("azure.identity", azure_identity)

azure_mgmt = ModuleType("azure.mgmt")
sys.modules.setdefault("azure.mgmt", azure_mgmt)
azure_cost = ModuleType("azure.mgmt.costmanagement")
azure_cost.CostManagementClient = object
sys.modules.setdefault("azure.mgmt.costmanagement", azure_cost)

azure_monitor = ModuleType("azure.monitor")
sys.modules.setdefault("azure.monitor", azure_monitor)
azure_monitor_query = ModuleType("azure.monitor.query")
azure_monitor_query.LogsQueryClient = object
sys.modules.setdefault("azure.monitor.query", azure_monitor_query)

# Stubs for other optional dependencies
numpy_stub = ModuleType("numpy")
numpy_stub.ndarray = object
sys.modules.setdefault("numpy", numpy_stub)
openai_stub = ModuleType("openai")
openai_stub.OpenAI = object
sys.modules.setdefault("openai", openai_stub)

from chatops.cli import app

runner = CliRunner()

class MockResponse:
    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text

    def json(self):
        return self._json_data

def test_deploy_success(monkeypatch):
    def mock_post(url, headers=None, json=None):
        return MockResponse(201)

    def mock_get(url, headers=None):
        data = {"workflow_runs": [{"id": 123, "status": "completed", "conclusion": "success"}]}
        return MockResponse(200, json_data=data)

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(time, "sleep", lambda s: None)

    env = {"GITHUB_TOKEN": "t", "GITHUB_REPOSITORY": "owner/repo"}
    result = runner.invoke(app, ["deploy", "deploy", "myapp", "prod"], env=env)

    assert result.exit_code == 0
    assert "Workflow dispatched" in result.output
    assert "Run 123 status: completed" in result.output

def test_deploy_api_error(monkeypatch):
    def mock_post(url, headers=None, json=None):
        return MockResponse(500, text="server error")

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(time, "sleep", lambda s: None)

    env = {"GITHUB_TOKEN": "t", "GITHUB_REPOSITORY": "owner/repo"}
    result = runner.invoke(app, ["deploy", "deploy", "myapp", "prod"], env=env)

    assert result.exit_code == 1
    assert "Failed to dispatch workflow" in result.output

def test_deploy_invalid_app(monkeypatch):
    def mock_post(url, headers=None, json=None):
        return MockResponse(422, text="Unprocessable Entity")

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(time, "sleep", lambda s: None)

    env = {"GITHUB_TOKEN": "t", "GITHUB_REPOSITORY": "owner/repo"}
    result = runner.invoke(app, ["deploy", "deploy", "badapp", "prod"], env=env)

    assert result.exit_code == 1
    assert "Failed to dispatch workflow" in result.output
