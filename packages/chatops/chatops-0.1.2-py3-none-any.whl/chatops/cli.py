import typer


from . import deploy, logs, cost, incident, security, cve

app = typer.Typer(help="ChatOps CLI")

app.add_typer(deploy.app, name="deploy")
app.add_typer(logs.app, name="logs")
app.add_typer(cost.app, name="cost")
app.add_typer(incident.app, name="incident")
app.add_typer(security.app, name="security")
app.add_typer(cve.app, name="cve")
