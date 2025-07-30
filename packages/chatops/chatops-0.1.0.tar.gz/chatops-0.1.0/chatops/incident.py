import os
import requests
import typer

app = typer.Typer(help="Incident management commands")

@app.command()
def list():
    """List open incidents with severity and time opened."""
    base_url = os.environ.get("INCIDENT_API_URL")
    token = os.environ.get("INCIDENT_API_TOKEN")
    if not base_url or not token:
        typer.echo("INCIDENT_API_URL and INCIDENT_API_TOKEN must be set")
        raise typer.Exit(code=1)

    url = f"{base_url.rstrip('/')}/incidents?status=open"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        typer.echo(f"Failed to fetch incidents: {resp.status_code} {resp.text}")
        raise typer.Exit(code=1)

    incidents = resp.json()
    if not incidents:
        typer.echo("No open incidents")
        raise typer.Exit()

    for incident in incidents:
        severity = incident.get("severity", "unknown")
        opened = incident.get("created_at") or incident.get("start_time")
        if opened:
            try:
                dt = datetime.fromisoformat(opened.replace("Z", "+00:00"))
                opened = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
        else:
            opened = "unknown"

        typer.echo(f"[{severity}] {opened}")
