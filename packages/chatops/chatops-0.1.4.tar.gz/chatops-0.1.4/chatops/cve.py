from datetime import datetime, timedelta, timezone
import requests
import typer

app = typer.Typer(help="CVE related commands")


@app.command()
def latest(limit: int = typer.Argument(5, help="Number of CVEs to display")):
    """Show latest high or critical vulnerabilities from NVD."""
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S.000")
    end = now.strftime("%Y-%m-%dT%H:%M:%S.000")
    params = {
        "cvssV3Severity": ["HIGH", "CRITICAL"],
        "resultsPerPage": limit,
        "pubStartDate": start,
        "pubEndDate": end,
    }
    try:
        resp = requests.get(
            "https://services.nvd.nist.gov/rest/json/cves/2.0", params=params, timeout=10
        )
    except Exception as e:
        typer.echo(f"Request failed: {e}")
        raise typer.Exit(code=1)
    if resp.status_code != 200:
        typer.echo(f"Failed to fetch CVEs: {resp.status_code}")
        raise typer.Exit(code=1)
    data = resp.json()
    vulns = data.get("vulnerabilities", [])
    if not vulns:
        typer.echo("No vulnerabilities found")
        raise typer.Exit()
    for v in vulns:
        cve = v.get("cve", {})
        cve_id = cve.get("id", "N/A")
        description = ""
        for desc in cve.get("descriptions", []):
            if desc.get("lang") == "en":
                description = desc.get("value")
                break
        score = None
        metrics = cve.get("metrics", {})
        for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            metric = metrics.get(key)
            if metric:
                score = metric[0].get("cvssData", {}).get("baseScore")
                if score is None:
                    score = metric[0].get("baseScore")
                if score is not None:
                    break
        typer.echo(f"{cve_id} - CVSS {score}")
        typer.echo(description)
        typer.echo("")
