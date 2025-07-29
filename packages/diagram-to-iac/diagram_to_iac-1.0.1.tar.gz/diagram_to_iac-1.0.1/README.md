# diagram-to-iac

> **"One container, many minds—zero manual toil."**

An automated DevOps-in-a-Box system that intelligently handles complete Repo-to-Deployment (R2D) workflows. The project combines AI-powered infrastructure analysis with GitHub automation for self-healing deployments.

## 🚀 DevOps-in-a-Box: R2D Action

The **R2D (Repo-to-Deployment) Action** is a self-healing, Terraform-first DevOps automation solution that lives inside a single GitHub Action. When you supply any repository URL, our SupervisorAgent marshals specialized agents to handle the complete deployment workflow.

### Quick Start with GitHub Actions

```yaml
name: Deploy Infrastructure
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy with R2D
        uses: amartyamandal/diagram-to-iac/.github/actions/r2d@v1
        with:
          repo: ${{ github.server_url }}/${{ github.repository }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TF_CLOUD_TOKEN: ${{ secrets.TF_CLOUD_TOKEN }}
```

### Key Features

- **🤖 Self-Healing**: Automatically creates GitHub Issues for errors and suggests fixes
- **🔒 Security-First**: Non-root container execution with workspace isolation
- **🌍 Multi-Cloud**: Supports Terraform, PowerShell, Bash, and Ansible deployments
- **📊 Observable**: Rich logging, step summaries, and artifact collection
- **🔄 Resumable**: Thread-based conversation tracking for workflow continuation
- **🧪 Testable**: Comprehensive dry-run mode for safe testing

### The Cast: Specialized Agents

| Agent | Capability | Never Does |
|-------|------------|------------|
| **SupervisorAgent** | Orchestrates workflow, manages checkpoints | Edit code directly |
| **GitAgent** | Clone, branch, PR creation, assign @github-copilot | Guess network credentials |
| **ShellAgent** | Safe command execution, stack detection | Execute non-allowlisted binaries |
| **TerraformAgent** | Init/plan/apply, error classification | Apply with critical security issues |
| **PolicyAgent** | tfsec + OPA security gates | Ignore critical findings |

## 📦 Installation

Create a virtual environment with Python 3.11+ and install the project in editable mode. Development dependencies (linting, testing, etc.) are provided through the `dev` extra:

```bash
pip install -e .[dev]
```

## 🖥️ Running the CLI

The project exposes several entry points via `pyproject.toml`:

### Main R2D CLI
```bash
# Run complete R2D workflow
diagram-to-iac https://github.com/user/repo
r2d-agent https://github.com/user/repo --dry-run

# Get help
diagram-to-iac --help
```

### Individual Agent CLIs
```bash
# SupervisorAgent (orchestration)
supervisor-agent --repo-url https://github.com/user/repo

# GitAgent (repository operations)
git-agent --repo-url https://github.com/user/repo

# TerraformAgent (infrastructure deployment)
terraform-agent --query "terraform plan"
```

### Interactive Mode

Running without arguments enters interactive mode:

```bash
$ supervisor-agent --dry-run
╔══════════════════════════════════════════════════════════════════════════════╗
║  🤖 DevOps-in-a-Box: SupervisorAgent                                        ║
║  "One container, many minds—zero manual toil."                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Repository URL: https://github.com/octocat/Hello-World.git
🚀 R2D SupervisorAgent - Workflow Orchestration
📅 Default branch name: r2d-<timestamp>
📝 Press Enter to use default, or type a custom branch name:
```

The agent will continue with the complete workflow (clone → detect → deploy → issue creation). The `--dry-run` flag simulates actions without making changes.

## Running Tests

All tests use `pytest` and are located under the `tests` directory. After installing the development dependencies, run:

```bash
pytest
```

## 📊 Logs and Observability

DevOps-in-a-Box provides comprehensive observability for all R2D workflows:

### Structured Logging
Each run creates a JSONL log file under the `logs/` directory (e.g. `logs/run-<timestamp>.jsonl`).
Every significant event is logged as structured JSON for easy parsing and analysis:

```bash
# Follow live logs
tail -f logs/run-*.jsonl

# Parse with jq for specific events
cat logs/run-*.jsonl | jq '. | select(.event_type == "terraform_apply")'
```

### Step Summary Dashboard
After each workflow, a Markdown dashboard is generated at `step-summary.md` with:
- 📈 Terraform resource changes and cost estimates
- 🔒 Security findings from tfsec/OPA scans
- 🏗️ Infrastructure modules and dependencies
- ⚡ Performance metrics and execution times

### GitHub Integration
- **Issues**: Automatically created for errors with detailed context
- **Pull Requests**: Auto-drafted fixes assigned to @github-copilot
- **Workflow Summaries**: Rich GitHub Actions step summaries
- **Artifacts**: Logs, plans, and reports uploaded for download

### CI/CD Artifacts
In GitHub Actions, the following artifacts are automatically collected:
- `logs/` - Structured JSONL logs
- `*.tfplan` - Terraform plan files  
- `step-summary.md` - Workflow dashboard
- `r2d-artifacts/` - Complete workflow artifacts

## 🔧 GitHub Actions Usage

Add the R2D action to your workflow for automated infrastructure deployment:

### Basic Setup

```yaml
name: Deploy Infrastructure
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy with R2D
        uses: amartyamandal/diagram-to-iac/.github/actions/r2d@v1
        with:
          repo: ${{ github.server_url }}/${{ github.repository }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TF_CLOUD_TOKEN: ${{ secrets.TF_CLOUD_TOKEN }}
```

### Advanced Configuration

```yaml
- name: Deploy with Custom Settings
  uses: amartyamandal/diagram-to-iac/.github/actions/r2d@v1
  with:
    repo: 'https://github.com/my-org/infrastructure'
    package_version: 'v2.1.0'
    dry_run: 'false'
    branch_name: 'deploy-prod'
    thread_id: 'prod-deployment-001'
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TF_CLOUD_TOKEN: ${{ secrets.TF_CLOUD_TOKEN }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Required Secrets

Configure these in your repository settings:

| Secret | Description | Required |
|--------|-------------|----------|
| `GITHUB_TOKEN` | GitHub API access (auto-provided) | ✅ Yes |
| `TF_CLOUD_TOKEN` | Terraform Cloud API token | ✅ Yes |
| `OPENAI_API_KEY` | OpenAI API key | ❌ Optional |
| `ANTHROPIC_API_KEY` | Claude API key | ❌ Optional |
| `GOOGLE_API_KEY` | Gemini API key | ❌ Optional |

### Example Workflows

See [`.github/actions/r2d/examples/`](.github/actions/r2d/examples/) for complete workflow examples:

- **Basic Deployment**: Simple push-to-deploy workflow
- **Multi-Environment**: Deploy to dev/staging/prod with approvals
- **PR Validation**: Validate infrastructure changes in pull requests
- **Drift Detection**: Scheduled infrastructure drift monitoring
- **External Repository**: Deploy from external repositories


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
