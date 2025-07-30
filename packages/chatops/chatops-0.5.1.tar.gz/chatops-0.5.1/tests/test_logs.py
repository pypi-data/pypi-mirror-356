from typer.testing import CliRunner
from chatops.cli import app

runner = CliRunner()

def test_logs_tail():
    result = runner.invoke(app, ["logs", "myservice"])
    assert result.exit_code == 0
    assert "log line" in result.output
