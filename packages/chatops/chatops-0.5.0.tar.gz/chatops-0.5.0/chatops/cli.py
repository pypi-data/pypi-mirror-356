import importlib.util
import typer
from pathlib import Path
from rich.console import Console
from . import (
    deploy,
    logs,
    cost,
    iam,
    incident,
    security,
    cve,
    suggest,
    monitor,
    explain,
    support,
    doctor,
    pr,
    changelog,
    history_cli,
    alias,
    config_cli,
    shell_cli,
    generate,
    agent,
    testing_cli,
    compliance,
    metrics,
    insight,
    audit,
    feedback,
    __version__,
)

app = typer.Typer(help="ChatOps CLI")

app.add_typer(deploy.app, name="deploy")
app.add_typer(logs.app, name="logs")
app.add_typer(cost.app, name="cost")
app.add_typer(iam.app, name="iam")
app.add_typer(incident.app, name="incident")
app.add_typer(security.app, name="security")
app.add_typer(cve.app, name="cve")
app.add_typer(explain.app, name="explain")
app.add_typer(monitor.app, name="monitor")
app.add_typer(support.app, name="support")
app.add_typer(doctor.app, name="doctor")
app.add_typer(pr.app, name="pr")
app.add_typer(changelog.app, name="changelog")
app.add_typer(history_cli.app, name="history")
app.add_typer(alias.app, name="alias")
app.add_typer(config_cli.app, name="config")
app.add_typer(shell_cli.app, name="shell")
app.add_typer(generate.app, name="generate")
app.add_typer(agent.app, name="agent")
app.add_typer(testing_cli.app, name="test")
app.add_typer(compliance.app, name="compliance")
app.add_typer(metrics.app, name="metrics")
app.add_typer(insight.app, name="insight")
app.add_typer(audit.app, name="audit")
app.add_typer(feedback.app, name="feedback")


def _load_plugins() -> None:
    plugin_dir = Path(".chatops/plugins")
    if not plugin_dir.exists():
        return
    for path in plugin_dir.glob("*.py"):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            plug_app = getattr(mod, "app", None)
            if isinstance(plug_app, typer.Typer):
                app.add_typer(plug_app, name=path.stem)


_load_plugins()


@app.command()
def version():
    """Show CLI version."""
    Console().print(__version__)
