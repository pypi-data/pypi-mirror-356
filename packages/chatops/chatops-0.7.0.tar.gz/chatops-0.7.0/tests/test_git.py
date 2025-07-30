from typer.testing import CliRunner
from chatops.cli import app

runner = CliRunner()

def test_git_status():
    result = runner.invoke(app, ["git", "status"])
    assert result.exit_code == 0
    assert "" in result.output

