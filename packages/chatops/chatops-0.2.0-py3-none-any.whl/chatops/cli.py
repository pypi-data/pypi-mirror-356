import typer
from . import deploy, logs, cost, iam, incident, security, cve, suggest, monitor, explain, support

app = typer.Typer(help="ChatOps CLI")

app.add_typer(deploy.app, name="deploy")
app.add_typer(logs.app, name="logs")
app.add_typer(cost.app, name="cost")
app.add_typer(iam.app, name="iam")
app.add_typer(incident.app, name="incident")
app.add_typer(security.app, name="security")
app.add_typer(cve.app, name="cve")
app.add_typer(suggest.app, name="suggest")
app.add_typer(explain.app, name="explain")
app.add_typer(monitor.app, name="monitor")
app.add_typer(support.app, name="support")
