# diagram-to-iac
An automated system that intelligently translates visual cloud infrastructure diagrams (specifically Azure) into deployable Infrastructure as Code (IaC). The project leverages AI for analysis and GitHub for collaborative refinement.

## Installation

Create a virtual environment with Python 3.11+ and install the project in editable mode. Development dependencies (linting, testing, etc.) are provided through the `dev` extra:

```bash
pip install -e .[dev]
```

## Running the CLI

The project exposes several entry points via `pyproject.toml`. The main one for end‑to‑end automation is `supervisor-agent`.

```bash
supervisor-agent --help
```

Running `supervisor-agent` without arguments enters an interactive mode. You will be prompted for the repository URL and branch name:

```bash
$ supervisor-agent --dry-run
Repository URL: https://github.com/octocat/Hello-World.git
🚀 R2D SupervisorAgent - Branch Creation
📅 Default branch name: r2d-<timestamp>
📝 Press Enter to use default, or type a custom branch name:
Branch name:
```

The agent will then continue with the workflow (cloning, analysis and issue creation). The `--dry-run` flag prints the generated issue text instead of creating it.

## Running Tests

All tests use `pytest` and are located under the `tests` directory. After installing the development dependencies, run:

```bash
pytest
```

## Logs and Observability

Each run creates a JSONL log file under the `logs/` directory (e.g. `logs/run-<timestamp>.jsonl`).
Every significant event emitted by the agents is appended as a single JSON line.
You can inspect the log with tools like `tail` to follow the workflow progress:

```bash
tail -f logs/run-*.jsonl
```


In CI runs, the `logs/` directory and any `*.tfplan` files are compressed and
uploaded as the `logs-and-plans` artifact. Download this artifact from the
workflow run to inspect full logs and Terraform plans.


After each workflow run, a Markdown dashboard is generated at `step-summary.md`
showing a high level overview of Terraform modules, resource changes and tfsec
findings. The dashboard is derived from the JSONL logs and can be viewed
directly in the repository or uploaded as a build artifact.



This repository provides a container action that runs the `SupervisorAgent` on the current repository. Add the action to a workflow as shown below:

```yaml
jobs:
  supervisor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Supervisor Agent
        uses: ./.github/actions/supervisor
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The action reads `GITHUB_REPOSITORY` and `GITHUB_TOKEN` automatically to clone the repository and execute the agent.
