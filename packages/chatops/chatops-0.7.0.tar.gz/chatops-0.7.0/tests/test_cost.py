from typer.testing import CliRunner
from chatops.cli import app

runner = CliRunner()

def test_cost_report():
    result = runner.invoke(app, ["cost", "report", "--to", "slack"])
    assert result.exit_code == 0
    assert "Cost report" in result.output
