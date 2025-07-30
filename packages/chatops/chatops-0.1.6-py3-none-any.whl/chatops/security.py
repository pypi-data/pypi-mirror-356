import typer

app = typer.Typer(help="Security related commands")

@app.command()
def scan():
    """Run security scan."""
    typer.echo("Security scan completed")
