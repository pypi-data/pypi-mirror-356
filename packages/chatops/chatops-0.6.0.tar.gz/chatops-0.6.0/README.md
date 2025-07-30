# chatops

A command line toolkit for operations teams built with [Typer](https://typer.tiangolo.com/).

## Installation

Install from PyPI:

```bash
pip install chatops
```

For local development from a cloned repository:

```bash
pip install -e .
```

Run tests with:

```bash
./test.sh
```

### Developer setup

```bash
git clone https://github.com/example/chatops.git
cd chatops
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Docker usage

Build and run the CLI in a container:

```bash
docker build -t chatops .
docker run --rm -v $PWD:/app chatops support --help
```

## Usage

Invoke the CLI with the installed entry point:

```bash
chatops --help
```

The command was previously named `chatops-toolkit`. That legacy name remains
available as an alias, but the recommended entry point is simply `chatops`.

You can also run the package directly:

```bash
python -m chatops --help
```

Both forms expose the same set of subcommands. Each command is invoked with the
`chatops` prefix:

- `chatops deploy` &ndash; deployment actions
- `chatops logs` &ndash; view recent logs
- `chatops cost` &ndash; cost management reports
- `chatops incident` &ndash; incident management
- `chatops security` &ndash; security utilities
- `chatops cve` &ndash; vulnerability information
- `chatops iam` &ndash; IAM utilities
- `chatops suggest` &ndash; AI helpers
- `chatops explain` &ndash; AI helpers
- `chatops monitor` &ndash; monitoring checks
- `chatops support` &ndash; interactive assistant
- `chatops doctor` &ndash; environment checks
- `chatops cloud` &ndash; cloud platform helpers
- `chatops git` &ndash; git workflow utilities
- `chatops docker` &ndash; Docker commands
- `chatops version` &ndash; show CLI version

### Command reference

#### deploy
- `chatops deploy deploy APP ENV` &ndash; trigger a GitHub Actions deployment workflow
- `chatops deploy status` &ndash; print deploy history
- `chatops deploy rollback APP ENV` &ndash; rollback to last release

#### logs
- `chatops logs SERVICE` &ndash; show recent log lines for a service
- `chatops logs live SERVICE` &ndash; stream live log lines
- `chatops logs grep PATTERN` &ndash; search log entries
- `chatops logs tail SERVICE [--lines N]` &ndash; tail logs (default 50 lines)

#### cost
- `chatops cost azure --subscription-id ID` &ndash; show Azure cost by service
- `chatops cost forecast` &ndash; show forecasted monthly spend
- `chatops cost top-spenders` &ndash; top 5 services by spend
- `chatops cost export [--format csv|json]` &ndash; export cost data

#### iam
- `chatops iam list-admins` &ndash; list IAM admins
- `chatops iam check-expired` &ndash; find expired credentials
- `chatops iam audit` &ndash; show IAM misconfigurations

#### incident
- `chatops incident ack INCIDENT_ID` &ndash; acknowledge an incident
- `chatops incident who` &ndash; show on-call rotation
- `chatops incident runbook TOPIC` &ndash; print SOP for a topic
- `chatops incident report create` &ndash; generate postmortem template

#### security
- `chatops security scan PATH` &ndash; scan for secrets
- `chatops security port-scan HOST` &ndash; scan open ports
- `chatops security whoami` &ndash; show cloud identity

#### cve
- `chatops cve latest` &ndash; fetch recent CVEs
- `chatops cve search --keyword TEXT` &ndash; search CVEs

#### suggest
- `chatops suggest PROMPT` &ndash; suggest best CLI command

- `chatops suggest explain TEXT` &ndash; explain an error message

#### explain
- `chatops explain explain TEXT` &ndash; explain a stack trace
- `chatops explain autofix FILE` &ndash; suggest code improvements

#### monitor
- `chatops monitor uptime URL` &ndash; check service uptime
- `chatops monitor latency [--threshold MS]` &ndash; simulate latency alert

#### support
- `chatops support` &ndash; launch interactive assistant (prompts for `OPENAI_API_KEY` if needed)

#### doctor
- `chatops doctor` &ndash; verify required tools are installed

#### generate
- `chatops generate terraform RESOURCE` &ndash; create Terraform config
- `chatops generate dockerfile` &ndash; produce a Dockerfile
- `chatops generate github-actions` &ndash; create CI workflow

#### agent
- `chatops agent run "if CPU > 80% -> scale"` &ndash; autonomous actions

#### test
- `chatops test write --file app.py` &ndash; generate tests
- `chatops test run` &ndash; run all tests

#### compliance
- `chatops compliance scan --profile cmmc` &ndash; simulate compliance checks

#### metrics
- `chatops metrics latency --service api` &ndash; show latency metrics

#### insight
- `chatops insight top-errors --window 1h` &ndash; recent log errors

#### feedback
- `chatops feedback --last up` &ndash; rate previous response

#### version
- `chatops version` &ndash; show CLI version

### Example commands

Deploy an application (requires `GITHUB_TOKEN` and `GITHUB_REPOSITORY`):

```bash
chatops deploy deploy myapp prod
```

Tail logs for a service:

```bash
chatops logs myservice
```

Generate an Azure cost report for a subscription:

```bash
chatops cost azure --subscription-id <SUBSCRIPTION_ID>
```

Show on-call rotation:

```bash
chatops incident who
```

Run a security scan:

```bash
chatops security scan .
```

Show recent pull requests for a repo:

```bash
chatops pr status owner/repo
```

Display command history:

```bash
chatops history show
```

Display high or critical CVEs published in the last week:

```bash
chatops cve latest
```

### Suggest a CLI Command

`suggest_command` maps natural language requests to a CLI command and requires `OPENAI_API_KEY`:

```python
from chatops import suggest_command

cmd = suggest_command("restart app on prod")
print(cmd)
```

### Plugins

Custom commands can be added by dropping ``*.py`` files in ``~/.chatops/plugins``
or ``.chatops/plugins`` within a project. Each plugin should expose a Typer
``app`` object. The CLI loads them automatically at startup and reports any
errors encountered during loading.

### Contributing

1. Fork the repository and create a virtual environment.
2. Install in editable mode with ``pip install -e .``.
3. Run ``./test.sh`` before submitting a pull request.
