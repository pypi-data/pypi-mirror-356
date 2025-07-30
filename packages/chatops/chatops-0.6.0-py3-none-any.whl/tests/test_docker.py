from typer.testing import CliRunner
from chatops.cli import app
import subprocess

runner = CliRunner()

def test_docker_scan(monkeypatch):
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **k: "")
    result = runner.invoke(app, ["docker", "scan", "--image", "app:latest"])
    assert result.exit_code == 0
    assert "no issues" in result.output
