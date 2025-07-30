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
- `iam` &ndash; IAM utilities
- `suggest` &ndash; AI helpers
- `explain` &ndash; AI helpers
- `monitor` &ndash; monitoring checks
- `support` &ndash; interactive assistant

### Command reference

#### deploy
- `deploy deploy APP ENV` &ndash; trigger a GitHub Actions deployment workflow
- `deploy status` &ndash; print deploy history
- `deploy rollback APP ENV` &ndash; rollback to last release

#### logs
- `logs live SERVICE` &ndash; stream live log lines
- `logs grep PATTERN` &ndash; search log entries
- `logs tail SERVICE [--lines N]` &ndash; tail logs (default 50 lines)

#### cost
- `cost azure --subscription-id ID` &ndash; show Azure cost by service
- `cost forecast` &ndash; show forecasted monthly spend
- `cost top-spenders` &ndash; top 5 services by spend
- `cost export [--format csv|json]` &ndash; export cost data

#### iam
- `iam list-admins` &ndash; list IAM admins
- `iam check-expired` &ndash; find expired credentials
- `iam audit` &ndash; show IAM misconfigurations

#### incident
- `incident ack INCIDENT_ID` &ndash; acknowledge an incident
- `incident who` &ndash; show on-call rotation
- `incident runbook TOPIC` &ndash; print SOP for a topic
- `incident report create` &ndash; generate postmortem template

#### security
- `security scan PATH` &ndash; scan for secrets
- `security port-scan HOST` &ndash; scan open ports
- `security whoami` &ndash; show cloud identity

#### cve
- `cve latest` &ndash; fetch recent CVEs
- `cve search --keyword TEXT` &ndash; search CVEs

#### suggest
- `suggest suggest PROMPT` &ndash; suggest best CLI command
- `suggest explain TEXT` &ndash; explain an error message

#### explain
- `explain explain TEXT` &ndash; explain a stack trace
- `explain autofix FILE` &ndash; suggest code improvements

#### monitor
- `monitor uptime URL` &ndash; check service uptime
- `monitor latency [--threshold MS]` &ndash; simulate latency alert

#### support
- `support support` &ndash; launch interactive assistant (prompts for `OPENAI_API_KEY` if needed)

### Example commands

Deploy an application (requires `GITHUB_TOKEN` and `GITHUB_REPOSITORY`):

```bash
chatops-toolkit deploy deploy myapp prod
```

Tail logs for a service:

```bash
python -m chatops logs tail myservice --lines 20
```

Generate an Azure cost report for a subscription:

```bash
python -m chatops cost azure --subscription-id <SUBSCRIPTION_ID>
```

Show on-call rotation:

```bash
python -m chatops incident who
```

Run a security scan:

```bash
python -m chatops security scan .
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
