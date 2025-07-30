# chatops-toolkit

A command line toolkit for operations teams built with [Typer](https://typer.tiangolo.com/).

## Installation

Install from PyPI:

```bash
pip install chatops-toolkit
```

## Usage

Invoke the CLI with the installed entry point:

```bash
chatops-toolkit
```

You can also run the package directly:

```bash
python -m chatops
```

### Suggest a CLI Command

The package exposes `suggest_command` to map natural language requests to a CLI command:

```python
from chatops import suggest_command

cmd = suggest_command("restart app on prod")
print(cmd)
```

### Latest CVEs

Display high or critical CVEs published in the last week:

```bash
python -m chatops cve latest
```
