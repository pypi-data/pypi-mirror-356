from typer.testing import CliRunner
from chatops.cli import app

runner = CliRunner()

def test_cloud_whoami_env(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "ABC")
    result = runner.invoke(app, ["cloud", "whoami", "--provider", "aws"])
    assert result.exit_code == 0
    assert "AWS access key" in result.output
