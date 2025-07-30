from typer.testing import CliRunner
from chatops.cli import app
import subprocess
from pathlib import Path
from chatops import env as env_mod, config

runner = CliRunner()

def test_docker_scan(monkeypatch, tmp_path):
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **k: "")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    cfg = tmp_path / ".chatops"
    monkeypatch.setattr(env_mod, "ACTIVE_FILE", cfg / ".active_env")
    monkeypatch.setattr(config, "CONFIG_FILE", cfg / "config.yaml")
    cfg.mkdir()
    (cfg / "config.yaml").write_text(
        "environments:\n  docker-local:\n    provider: docker\n"
    )
    (cfg / ".active_env").write_text("docker-local")
    result = runner.invoke(app, ["docker", "scan", "--image", "app:latest"])
    assert result.exit_code == 0
    assert "no issues" in result.output

