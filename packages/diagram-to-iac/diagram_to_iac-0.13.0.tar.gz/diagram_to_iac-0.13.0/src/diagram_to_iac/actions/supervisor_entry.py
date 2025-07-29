"""CLI entrypoint for SupervisorAgent."""

import argparse
import json
import sys
import logging
from datetime import datetime
from pathlib import Path

from diagram_to_iac.agents.supervisor_langgraph import (
    SupervisorAgent,
    SupervisorAgentInput,
)
from diagram_to_iac.services import get_log_path, generate_step_summary, reset_log_bus


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="supervisor-agent",
        description="SupervisorAgent CLI - R2D (Repo-to-Deployment) automation",
    )
    parser.add_argument("--repo-url", help="Repository URL to operate on")
    parser.add_argument("--branch-name", help="Branch name (deprecated - supervisor skips branch creation)")
    parser.add_argument("--thread-id", help="Optional thread id")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--no-interactive", action="store_true", help="Skip interactive prompts")
    parser.add_argument("--dry-run", action="store_true", help="Print issue text instead of creating it")
    return parser


def prompt_for_repo_url() -> str:
    """Prompt the user for a repository URL."""
    try:
        return input("Repository URL: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n⚠️  Repository URL required")
        sys.exit(1)


def format_output(result: object) -> str:
    try:
        if hasattr(result, "model_dump"):
            return json.dumps(result.model_dump(), indent=2)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        logging.warning(f"Failed to serialize output: {e}")
        return str(result)


def main() -> int:
    parser = create_argument_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)

    # Handle repo url
    repo_url = args.repo_url
    if not repo_url and not args.no_interactive:
        repo_url = prompt_for_repo_url()
    elif not repo_url:
        parser.error("--repo-url is required when --no-interactive is used")

    # Branch name is no longer used since supervisor skips branch creation
    # All errors are handled via GitHub issues instead
    branch_name = args.branch_name or "main"  # Placeholder for compatibility

    agent = SupervisorAgent()


    while True:
        reset_log_bus()
        result = agent.run(
            SupervisorAgentInput(
                repo_url=repo_url,
                branch_name=branch_name,
                thread_id=args.thread_id,
                dry_run=args.dry_run,
            )

        )

        print(format_output(result))

        try:
            generate_step_summary(get_log_path(), Path("step-summary.md"))
        except Exception as e:  # noqa: BLE001
            logging.warning(f"Step summary generation failed: {e}")

        if result.success or args.no_interactive:
            break

        try:
            choice = input("Retry workflow? [y/N]: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            choice = ""

        if choice != "y":
            break

        repo_url = prompt_for_repo_url()
        # No longer prompt for branch name since supervisor skips branch creation

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
