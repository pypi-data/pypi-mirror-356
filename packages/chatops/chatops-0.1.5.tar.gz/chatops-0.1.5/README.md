# chatops-toolkit

A command line toolkit for operations teams built with [Typer](https://typer.tiangolo.com/).

## Installation

Install from PyPI:

```bash
pip install chatops
```

## Usage

Invoke the CLI with the installed entry point:

```bash
chatops-toolkit --help
```

You can also run the package directly:

```bash
python -m chatops --help
```

Both forms expose the same set of subcommands:

- `deploy` &ndash; deployment actions
- `logs` &ndash; view recent logs
- `cost` &ndash; cost management reports
- `incident` &ndash; incident management
- `security` &ndash; security utilities
- `cve` &ndash; vulnerability information

### Example commands

Deploy an application (requires `GITHUB_TOKEN` and `GITHUB_REPOSITORY`):

```bash
chatops-toolkit deploy deploy myapp prod
```

Show recent log entries:

```bash
python -m chatops logs show
```

Generate an Azure cost report for a subscription:

```bash
python -m chatops cost report azure <SUBSCRIPTION_ID>
```

List open incidents (requires `INCIDENT_API_URL` and `INCIDENT_API_TOKEN`):

```bash
python -m chatops incident list
```

Run a security scan:

```bash
python -m chatops security scan
```

Display high or critical CVEs published in the last week:

```bash
python -m chatops cve latest
```

### Suggest a CLI Command

`suggest_command` maps natural language requests to a CLI command and requires `OPENAI_API_KEY`:

```python
from chatops import suggest_command

cmd = suggest_command("restart app on prod")
print(cmd)
```
