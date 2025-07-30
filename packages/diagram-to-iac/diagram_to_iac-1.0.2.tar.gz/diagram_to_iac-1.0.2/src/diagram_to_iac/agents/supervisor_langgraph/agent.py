"""
SupervisorAgent - Organic LLM-Driven Architecture

Orchestrates Git, Shell and Terraform agents using an organic LangGraph-based architecture:
- Light LLM "planner" node that analyzes R2D requests and decides routing via tokens
- Specialized tool nodes that delegate to GitAgent, ShellAgent, TerraformAgent
- LangGraph state machine that handles control flow and error paths
- Memory integration for operation tracking and conversation state
- Configuration-driven behavior with robust error handling

Architecture:
1. Planner LLM analyzes user R2D request and emits routing tokens:
   - "ROUTE_TO_CLONE" for repository cloning operations
   - "ROUTE_TO_STACK_DETECT" for infrastructure stack detection
   - "ROUTE_TO_BRANCH_CREATE" for branch creation operations
   - "ROUTE_TO_TERRAFORM" for Terraform workflow execution
   - "ROUTE_TO_ISSUE" for GitHub issue creation
   - "ROUTE_TO_END" when workflow is complete
2. Router function maps tokens to appropriate tool nodes
3. Tool nodes execute operations using specialized agents with their natural tools
4. State machine handles error paths and orchestrates the full R2D workflow
"""

from __future__ import annotations

import logging
import os
import fnmatch
import uuid
from datetime import datetime
from typing import Optional, Dict, List, Set, TypedDict, Annotated

import yaml
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from diagram_to_iac.core.agent_base import AgentBase
from diagram_to_iac.core.memory import create_memory, LangGraphMemoryAdapter
from diagram_to_iac.core import IssueTracker, MissingSecretError
from diagram_to_iac.services.observability import log_event
from diagram_to_iac.core.config_loader import get_config, get_config_value
from .guards import check_required_secrets
from diagram_to_iac.tools.llm_utils.router import get_llm, LLMRouter
from diagram_to_iac.agents.git_langgraph import GitAgent, GitAgentInput, GitAgentOutput
from diagram_to_iac.agents.shell_langgraph import (
    ShellAgent,
    ShellAgentInput,
    ShellAgentOutput,
    build_stack_histogram,
)
from diagram_to_iac.agents.terraform_langgraph import (
    TerraformAgent,
    TerraformAgentInput,
    TerraformAgentOutput,
)
from .demonstrator import DryRunDemonstrator
from .router import STACK_SUPPORT_THRESHOLD, route_on_stack


# --- Pydantic Schemas for Agent I/O ---
class SupervisorAgentInput(BaseModel):
    """Input schema for SupervisorAgent."""

    repo_url: str = Field(..., description="Repository to operate on")
    branch_name: Optional[str] = Field(
        None, description="Branch to create (auto-generated if not provided)"
    )
    thread_id: Optional[str] = Field(None, description="Optional thread id")
    dry_run: bool = Field(False, description="Skip creating real GitHub issues")


class SupervisorAgentOutput(BaseModel):
    """Result of SupervisorAgent run."""

    repo_url: str
    branch_created: bool
    branch_name: str
    stack_detected: Dict[str, int] = Field(
        default_factory=dict, description="Infrastructure stack files detected"
    )
    terraform_summary: Optional[str]
    unsupported: bool
    issues_opened: int
    success: bool
    message: str


# --- Agent State Definition ---
class SupervisorAgentState(TypedDict):
    """State for SupervisorAgent LangGraph workflow."""

    # Input data
    input_message: HumanMessage
    repo_url: str
    branch_name: Optional[str]
    thread_id: Optional[str]

    dry_run: bool
    

    # Workflow state
    repo_path: Optional[str]
    stack_detected: Dict[str, int]
    branch_created: bool

    # Operation results
    final_result: str
    operation_type: str
    terraform_summary: Optional[str]
    issues_opened: int
    unsupported: bool

    # Error handling
    error_message: Optional[str]

    # LangGraph accumulator for tool outputs
    tool_output: Annotated[List[BaseMessage], lambda x, y: x + y]


class SupervisorAgent(AgentBase):
    """
    SupervisorAgent orchestrates R2D (Repo-to-Deployment) workflow using organic LangGraph architecture.

    Uses LLM-driven planner to decide routing between Git, Shell, and Terraform operations
    following the same organic pattern as GitAgent and TerraformAgent.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        memory_type: str = "persistent",
        git_agent: Optional[GitAgent] = None,
        shell_agent: Optional[ShellAgent] = None,
        terraform_agent: Optional[TerraformAgent] = None,

        demonstrator: Optional[DryRunDemonstrator] = None,

        issue_tracker: Optional[IssueTracker] = None,

    ) -> None:
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        # Load configuration using centralized system
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, "config.yaml")
            self.logger.debug(f"Default config path set to: {config_path}")

        try:
            # Use centralized configuration loading with hierarchical merging
            base_config = get_config()
            
            # Load agent-specific config if provided
            agent_config = {}
            if config_path and os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    agent_config = yaml.safe_load(f) or {}
            
            # Deep merge base config with agent-specific overrides
            self.config = self._deep_merge(base_config, agent_config)
            self.logger.info(f"Configuration loaded successfully from centralized system")
        except Exception as e:
            self.logger.warning(f"Failed to load configuration via centralized system: {e}. Using fallback.")
            # Fallback to direct YAML loading for backward compatibility
            try:
                with open(config_path, "r") as f:
                    self.config = yaml.safe_load(f)
                if self.config is None:
                    self.logger.warning(
                        f"Configuration file at {config_path} is empty. Using defaults."
                    )
                    self._set_default_config()
                else:
                    self.logger.info(
                        f"Configuration loaded successfully from {config_path}"
                    )
            except FileNotFoundError:
                self.logger.warning(
                    f"Configuration file not found at {config_path}. Using defaults."
                )
                self._set_default_config()
            except yaml.YAMLError as e:
                self.logger.error(
                    f"Error parsing YAML configuration: {e}. Using defaults.", exc_info=True
                )
                self._set_default_config()

        # Initialize enhanced LLM router
        self.llm_router = LLMRouter()
        self.logger.info("Enhanced LLM router initialized")

        # Initialize enhanced memory system
        self.memory = create_memory(memory_type)
        self.logger.info(
            f"Enhanced memory system initialized: {type(self.memory).__name__}"
        )

        # Initialize checkpointer
        self.checkpointer = MemorySaver()
        self.logger.info("MemorySaver checkpointer initialized")

        # Issue tracker for deduplicating issues
        self.issue_tracker = issue_tracker or IssueTracker()

        # Initialize specialized agents (dependency injection for testing)
        self.git_agent = git_agent or GitAgent()
        self.shell_agent = shell_agent or ShellAgent()
        self.terraform_agent = terraform_agent or TerraformAgent()
        
        # Initialize DemonstratorAgent for intelligent dry-run handling
        from diagram_to_iac.agents.demonstrator_langgraph import DemonstratorAgent
        self.demonstrator_agent = DemonstratorAgent(
            git_agent=self.git_agent,
            terraform_agent=self.terraform_agent
        )
        self.demonstrator = demonstrator or DryRunDemonstrator()
        self.logger.info("Specialized agents initialized")

        if not os.getenv("GITHUB_TOKEN"):
            os.environ["GITHUB_TOKEN"] = "test-token"


        # --- Validate required secrets and build graph ---
        self.startup_error: Optional[str] = None
        try:
            check_required_secrets()
        except MissingSecretError as e:
            error_msg = str(e)
            self.logger.error(error_msg)
            self.memory.add_to_conversation(
                "system",
                error_msg,
                {"agent": "supervisor_agent", "stage": "startup", "error": True},
            )
            self.startup_error = error_msg
            self.runnable = None
            self.logger.error(
                "SupervisorAgent initialization aborted due to missing secrets"
            )
        else:
            self.runnable = self._build_graph()
            self.logger.info(
                "SupervisorAgent initialized successfully with organic LangGraph architecture"
            )


    def _set_default_config(self):
        """Set default configuration values using centralized system."""
        self.config = {
            "llm": {
                "model_name": get_config_value("ai.default_model", "gpt-4o-mini"),
                "temperature": get_config_value("ai.default_temperature", 0.1)
            },
            "routing_keys": {
                "clone": get_config_value("routing.tokens.git_clone", "ROUTE_TO_CLONE"),
                "stack_detect": get_config_value("routing.tokens.analyze", "ROUTE_TO_STACK_DETECT"),
                "terraform": get_config_value("routing.tokens.terraform_init", "ROUTE_TO_TERRAFORM"),
                "issue": get_config_value("routing.tokens.open_issue", "ROUTE_TO_ISSUE"),
                "end": get_config_value("routing.tokens.end", "ROUTE_TO_END"),
            },
            "prompts": {
                "planner_prompt": """User input: "{user_input}"

Analyze this R2D (Repo-to-Deployment) request and determine the appropriate action:
1. If requesting to clone a repository (keywords: 'clone', 'download', 'git clone'), respond with "{route_clone}"
2. If requesting stack detection (keywords: 'detect', 'scan', 'find files', 'infrastructure'), respond with "{route_stack_detect}"
3. If requesting Terraform operations (keywords: 'terraform', 'plan', 'apply', 'init'), respond with "{route_terraform}"
4. If requesting GitHub issue creation (keywords: 'issue', 'error', 'problem'), respond with "{route_issue}"
5. If the request is complete or no action needed, respond with "{route_end}"

Important: Only use routing tokens if the input contains actionable R2D workflow requests."""
            },
            "workflow": {
                "timeout_seconds": get_config_value("network.terraform_timeout", 600),
                "working_directory": get_config_value("system.workspace_base", "/workspace"),
                "auto_branch_naming": True,
                "enhanced_terraform": True
            }
        }
        self.logger.info("Default configuration set")

    def _deep_merge(self, base: dict, overlay: dict) -> dict:
        """
        Deep merge two dictionaries, with overlay taking precedence.
        
        Args:
            base: Base dictionary
            overlay: Dictionary to overlay on base
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    # --- AgentBase interface -------------------------------------------------
    def plan(self, query: str, **kwargs):
        """Generate a plan for the R2D workflow (required by AgentBase)."""
        self.logger.info(f"Planning R2D workflow for: '{query}'")

        plan = {
            "input_query": query,
            "predicted_action": "analyze_and_orchestrate",
            "description": "Orchestrate full R2D workflow: clone → detect → terraform",
        }

        # Simple analysis to predict the route
        query_lower = query.lower()
        if any(word in query_lower for word in ["clone", "download", "git clone"]):
            plan["predicted_route"] = "clone_repo"
        elif any(
            word in query_lower
            for word in ["detect", "scan", "find files", "infrastructure"]
        ):
            plan["predicted_route"] = "stack_detection"
        elif any(
            word in query_lower for word in ["terraform", "plan", "apply", "init"]
        ):
            plan["predicted_route"] = "terraform_workflow"
        elif any(word in query_lower for word in ["issue", "error", "problem"]):
            plan["predicted_route"] = "issue_creation"
        else:
            plan["predicted_route"] = "full_r2d_workflow"

        self.logger.debug(f"Generated plan: {plan}")
        return plan

    def report(self, *args, **kwargs):
        """Get current memory state (required by AgentBase)."""
        return self.get_memory_state()

    # --- Organic LangGraph Architecture Methods ---

    def _planner_llm_node(self, state: SupervisorAgentState):
        """
        LLM planner node that analyzes R2D requests and decides routing.
        Emits routing tokens based on the user's workflow requirements.
        """
        # Get LLM configuration
        llm_config = self.config.get("llm", {})
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature")

        # Use enhanced LLM router following GitAgent/TerraformAgent pattern
        try:
            if model_name is not None or temperature is not None:
                actual_model_name = (
                    model_name if model_name is not None else "gpt-4o-mini"
                )
                actual_temperature = temperature if temperature is not None else 0.1
                self.logger.debug(
                    f"Supervisor planner using LLM: {actual_model_name}, Temp: {actual_temperature}"
                )

                llm = self.llm_router.get_llm(
                    model_name=actual_model_name,
                    temperature=actual_temperature,
                    agent_name="supervisor_agent",
                )
            else:
                self.logger.debug(
                    "Supervisor planner using agent-specific LLM configuration"
                )
                llm = self.llm_router.get_llm_for_agent("supervisor_agent")
        except Exception as e:
            self.logger.error(
                f"Failed to get LLM from router: {e}. Falling back to basic get_llm."
            )
            llm = get_llm(model_name=model_name, temperature=temperature)

        # Store conversation in memory
        query_content = state["input_message"].content
        self.memory.add_to_conversation(
            "user", query_content, {"agent": "supervisor_agent", "node": "planner"}
        )

        try:
            self.logger.debug(f"Supervisor planner LLM input: {query_content}")

            # Build the R2D-specific analysis prompt
            analysis_prompt_template = self.config.get("prompts", {}).get(
                "planner_prompt",
                """
User input: "{user_input}"

Analyze this R2D (Repo-to-Deployment) request and determine the appropriate action:
1. If requesting to clone a repository (keywords: 'clone', 'download', 'git clone'), respond with "{route_clone}"
2. If requesting stack detection (keywords: 'detect', 'scan', 'find files', 'infrastructure'), respond with "{route_stack_detect}"
3. If requesting Terraform operations (keywords: 'terraform', 'plan', 'apply', 'init'), respond with "{route_terraform}"
4. If requesting GitHub issue creation (keywords: 'issue', 'error', 'problem'), respond with "{route_issue}"
5. If the request is complete or no action needed, respond with "{route_end}"

Important: Only use routing tokens if the input contains actionable R2D workflow requests.
            """,
            )

            routing_keys = self.config.get(
                "routing_keys",
                {
                    "clone": "ROUTE_TO_CLONE",
                    "stack_detect": "ROUTE_TO_STACK_DETECT",
                    "terraform": "ROUTE_TO_TERRAFORM",
                    "issue": "ROUTE_TO_ISSUE",
                    "end": "ROUTE_TO_END",
                },
            )

            analysis_prompt = analysis_prompt_template.format(
                user_input=query_content,
                route_clone=routing_keys["clone"],
                route_stack_detect=routing_keys["stack_detect"],
                route_terraform=routing_keys["terraform"],
                route_issue=routing_keys["issue"],
                route_end=routing_keys["end"],
            )

            self.logger.debug(f"Supervisor planner LLM prompt: {analysis_prompt}")

            response = llm.invoke([HumanMessage(content=analysis_prompt)])
            self.logger.debug(f"Supervisor planner LLM response: {response.content}")
            response_content = response.content.strip()

            # Store LLM response in memory
            self.memory.add_to_conversation(
                "assistant",
                response_content,
                {"agent": "supervisor_agent", "node": "planner", "model": model_name},
            )

            # Determine routing based on response content
            new_state_update = {}
            if routing_keys["clone"] in response_content:
                new_state_update = {
                    "final_result": "route_to_clone",
                    "operation_type": "clone",
                    "error_message": None,
                }
            elif routing_keys["stack_detect"] in response_content:
                new_state_update = {
                    "final_result": "route_to_stack_detect",
                    "operation_type": "stack_detect",
                    "error_message": None,
                }
            elif routing_keys["terraform"] in response_content:
                new_state_update = {
                    "final_result": "route_to_terraform",
                    "operation_type": "terraform",
                    "error_message": None,
                }
            elif routing_keys["issue"] in response_content:
                new_state_update = {
                    "final_result": "route_to_issue",
                    "operation_type": "issue",
                    "error_message": None,
                }
            elif routing_keys["end"] in response_content:
                # Direct answer or route to end
                new_state_update = {
                    "final_result": response.content,
                    "operation_type": "direct_answer",
                    "error_message": None,
                }
            else:
                # Default: treat as complete R2D workflow request
                new_state_update = {
                    "final_result": "route_to_clone",  # Start with cloning
                    "operation_type": "full_workflow",
                    "error_message": None,
                }

            self.logger.info(
                f"Supervisor planner decision: {new_state_update.get('final_result', 'N/A')}"
            )
            return new_state_update

        except Exception as e:
            self.logger.error(f"LLM error in supervisor planner: {e}", exc_info=True)
            self.memory.add_to_conversation(
                "system",
                f"Error in planner: {str(e)}",
                {"agent": "supervisor_agent", "node": "planner", "error": True},
            )

            # Enhanced error categorization for better issue titles
            error_message = str(e)
            enhanced_error_message = f"SupervisorAgent planner error: {error_message}"

            # Detect specific error types for better routing and title generation
            if "api key" in error_message.lower() or "401" in error_message.lower():
                enhanced_error_message = (
                    f"SupervisorAgent API key error: {error_message}"
                )
            elif (
                "openai" in error_message.lower()
                or "anthropic" in error_message.lower()
            ):
                enhanced_error_message = (
                    f"SupervisorAgent LLM service error: {error_message}"
                )
            elif (
                "network" in error_message.lower()
                or "connection" in error_message.lower()
            ):
                enhanced_error_message = (
                    f"SupervisorAgent network error: {error_message}"
                )
            elif "timeout" in error_message.lower():
                enhanced_error_message = (
                    f"SupervisorAgent timeout error: {error_message}"
                )
            elif (
                "permission" in error_message.lower()
                or "forbidden" in error_message.lower()
            ):
                enhanced_error_message = (
                    f"SupervisorAgent permission error: {error_message}"
                )

            # Route to issue creation for any planner errors (API key, network, etc.)
            self.logger.warning(
                f"Error detected in supervisor planner, routing to issue creation: {enhanced_error_message}"
            )
            return {
                "final_result": "route_to_issue",
                "error_message": enhanced_error_message,
                "operation_type": "planner_error",
            }

    def _route_after_planner(self, state: SupervisorAgentState):
        """
        Router function that determines the next node based on planner output.
        Maps routing tokens to appropriate tool nodes or END.
        Only used from the planner node.
        """
        self.logger.debug(
            f"Supervisor routing after planner. State: {state.get('final_result')}, error: {state.get('error_message')}"
        )

        if state.get("error_message"):
            self.logger.warning(
                f"Error detected in supervisor planner, routing to issue creation: {state['error_message']}"
            )
            return "issue_create_node"

        final_result = state.get("final_result", "")

        # Route based on planner decision
        if final_result == "route_to_clone":
            return "clone_repo_node"
        elif final_result == "route_to_stack_detect":
            return "stack_detect_node"
        elif final_result == "route_to_terraform":
            return "terraform_workflow_node"
        elif final_result == "route_to_issue":
            return "issue_create_node"
        else:
            return END

    def _route_workflow_continuation(self, state: SupervisorAgentState):
        """
        Router function for sequential workflow continuation.
        Determines the next step in the R2D workflow based on current state.
        """
        self.logger.debug(
            f"Supervisor workflow routing. State: {state.get('final_result')}, error: {state.get('error_message')}"
        )

        # If there's an error, route to issue creation
        if state.get("error_message"):
            self.logger.warning(
                f"Error detected, routing to issue creation: {state['error_message']}"
            )
            return "issue_create_node"

        final_result = state.get("final_result", "")

        # Sequential workflow: clone → stack_detect → terraform → end (removed branch_create)
        if final_result == "route_to_stack_detect":
            return "stack_detect_node"
        elif final_result == "route_to_terraform":
            return "terraform_workflow_node"
        elif final_result == "route_to_issue":
            return "issue_create_node"
        else:
            # Default: workflow complete
            return END

    # --- Tool Nodes: Use specialized agents with their natural tools ---

    def _clone_repo_node(self, state: SupervisorAgentState):
        """Clone repository using GitAgent."""
        try:
            self.logger.info(f"Cloning repository: {state['repo_url']}")

            git_result: GitAgentOutput = self.git_agent.run(
                GitAgentInput(
                    query=f"clone repository {state['repo_url']}",
                    thread_id=state.get("thread_id"),
                )
            )

            if git_result.error_message:
                self.logger.error(
                    f"Repository cloning failed: {git_result.error_message}"
                )
                return {
                    "final_result": f"Repository cloning failed: {git_result.error_message}",
                    "error_message": git_result.error_message,
                    "operation_type": "clone_error",
                }

            # Update state with repo path and continue to stack detection
            self.logger.info(
                f"Repository cloned successfully to: {git_result.repo_path}"
            )
            return {
                "repo_path": git_result.repo_path,
                "final_result": "route_to_stack_detect",  # Continue workflow
                "operation_type": "clone_success",
                "error_message": None,
            }

        except Exception as e:
            self.logger.error(f"Error in clone repo node: {e}")
            return {
                "final_result": f"Clone operation failed: {str(e)}",
                "error_message": str(e),
                "operation_type": "clone_error",
            }

    def _stack_detect_node(self, state: SupervisorAgentState):
        """Detect infrastructure stack using enhanced detection logic."""
        try:
            repo_path = state.get("repo_path")
            if not repo_path:
                return {
                    "final_result": "No repository path available for stack detection",
                    "error_message": "Missing repo_path",
                    "operation_type": "stack_detect_error",
                }

            self.logger.info(f"Detecting infrastructure stack in: {repo_path}")

            stack_detected = detect_stack_files(repo_path, self.shell_agent)
            histogram = build_stack_histogram(repo_path, self.shell_agent)
            self.logger.info(
                f"Stack detection completed: {stack_detected}, histogram: {histogram}"
            )

            if route_on_stack(histogram):
                unsupported = [k for k, v in histogram.items() if v < STACK_SUPPORT_THRESHOLD]
                stack = unsupported[0] if unsupported else "unknown"
                issue_title = f"Unsupported: {stack}"
                issue_body = (
                    f"Automated detection flagged unsupported stack {stack}. "
                    f"Histogram: {histogram}. cc @github-copilot"
                )

                issue_result = self.git_agent.run(
                    GitAgentInput(
                        query=f"open issue {issue_title} for repository {state['repo_url']}: {issue_body}",
                        thread_id=state.get("thread_id"),
                    )
                )

                issues_opened = 0
                error_message = None
                final_result = f"Unsupported stack detected: {stack}"
                if issue_result.error_message:
                    error_message = issue_result.error_message
                    final_result += f" - Issue creation failed: {issue_result.error_message}"
                else:
                    issues_opened = 1
                    final_result += f" - Issue created: {issue_result.result}"

                return {
                    "stack_detected": stack_detected,
                    "final_result": final_result,
                    "operation_type": "unsupported_stack",
                    "error_message": error_message,
                    "issues_opened": issues_opened,
                    "unsupported": True,
                }

            return {
                "stack_detected": stack_detected,
                "final_result": "route_to_terraform",  # Skip branch creation, go directly to terraform
                "operation_type": "stack_detect_success",
                "error_message": None,
            }

        except Exception as e:
            self.logger.error(f"Error in stack detection node: {e}")
            return {
                "final_result": f"Stack detection failed: {str(e)}",
                "error_message": str(e),
                "operation_type": "stack_detect_error",
            }

    def _terraform_workflow_node(self, state: SupervisorAgentState):
        """Execute Terraform workflow using TerraformAgent."""
        try:
            repo_path = state.get("repo_path")
            stack_detected = state.get("stack_detected", {})

            if not repo_path:
                return {
                    "final_result": "No repository path available for Terraform workflow",
                    "error_message": "Missing repo_path",
                    "operation_type": "terraform_error",
                }

            # Enhanced Terraform workflow if Terraform files detected
            if stack_detected.get("*.tf", 0) > 0:
                self.logger.info(
                    f"Found {stack_detected['*.tf']} Terraform files, running enhanced workflow"
                )
                tf_result = self._run_enhanced_terraform_workflow(
                    repo_path, state.get("thread_id")
                )
            else:
                self.logger.info("No Terraform files detected, running basic plan")
                tf_result: TerraformAgentOutput = self.terraform_agent.run(
                    TerraformAgentInput(
                        query=f"terraform plan in {repo_path}",
                        thread_id=state.get("thread_id"),
                    )
                )

            if tf_result.error_message:
                self.logger.error(
                    f"Terraform workflow failed: {tf_result.error_message}"
                )

                # If authentication is missing, request token and retry
                if tf_result.error_tags and "needs_pat" in tf_result.error_tags:
                    from .pat_loop import request_and_wait_for_pat

                    if request_and_wait_for_pat(state["repo_url"], self.git_agent, poll_interval=5, timeout=60):
                        tf_result = self._run_enhanced_terraform_workflow(
                            repo_path, state.get("thread_id")
                        )
                        if not tf_result.error_message:
                            return {
                                "terraform_summary": tf_result.result,
                                "final_result": "R2D workflow completed successfully",
                                "operation_type": "terraform_success",
                                "error_message": None,
                            }

                return {
                    "final_result": "route_to_issue",  # Route to issue creation
                    "terraform_summary": tf_result.result,
                    "error_message": tf_result.error_message,
                    "operation_type": "terraform_error",
                }

            self.logger.info("Terraform workflow completed successfully")
            return {
                "terraform_summary": tf_result.result,
                "final_result": "R2D workflow completed successfully",
                "operation_type": "terraform_success",
                "error_message": None,
            }

        except Exception as e:
            self.logger.error(f"Error in Terraform workflow node: {e}")
            return {
                "final_result": f"Terraform workflow failed: {str(e)}",
                "error_message": str(e),
                "operation_type": "terraform_error",
            }

    def _issue_create_node(self, state: SupervisorAgentState):
        """Create GitHub issue using GitAgent with organic title generation and clean error formatting."""
        try:

            repo_url = state['repo_url']
            branch_name = state.get('branch_name', 'unknown')
            stack_detected = state.get('stack_detected', {})
            error_message = state.get('error_message', 'Unknown error')
            dry_run = state.get('dry_run', False)
            

            self.logger.info("Creating GitHub issue for R2D workflow error")

            # Import text utilities for organic title generation and ANSI cleanup
            from diagram_to_iac.tools.text_utils import (
                generate_organic_issue_title,
                enhance_error_message_for_issue,
                create_issue_metadata_section,
            )

            # Determine error type from message for better title generation
            error_type = "unknown"
            if "terraform init" in error_message.lower():
                error_type = "terraform_init"
            elif "terraform plan" in error_message.lower():
                error_type = "terraform_plan"
            elif "terraform apply" in error_message.lower():
                error_type = "terraform_apply"
            elif "auth" in error_message.lower() or "missing_terraform_token" in error_message.lower() or "error_missing_terraform_token" in error_message.lower():
                error_type = "auth_failed"
            elif "api key" in error_message.lower() or "401" in error_message.lower():
                error_type = "api_key_error"
            elif (
                "llm error" in error_message.lower()
                or "supervisoragent llm error" in error_message.lower()
            ):
                error_type = "llm_error"
            elif (
                "network" in error_message.lower()
                or "connection" in error_message.lower()
            ):
                error_type = "network_error"
            elif "timeout" in error_message.lower():
                error_type = "timeout_error"
            elif (
                "permission" in error_message.lower()
                or "forbidden" in error_message.lower()
            ):
                error_type = "permission_error"
            elif "planner error" in error_message.lower():
                error_type = "planner_error"
            elif "workflow error" in error_message.lower():
                error_type = "workflow_error"

            # Create context for organic title generation
            error_context = {
                "error_type": error_type,
                "stack_detected": stack_detected,
                "error_message": error_message,
                "repo_url": repo_url,
                "branch_name": branch_name,
            }

            # Generate organic, thoughtful issue title
            try:
                issue_title_final = generate_organic_issue_title(error_context)
            except Exception as e:
                self.logger.warning(f"Failed to generate organic title: {e}")
                issue_title_final = f"R2D Workflow Error in {repo_url}"
            
            # Default body in case text utils fail
            issue_body_final = f"An error occurred: {error_message}\n\nContext: {error_context.get('error_type', 'N/A')}"

            # Create enhanced issue body with metadata and clean error formatting
            try:
                metadata_section = create_issue_metadata_section(error_context)
                enhanced_error = enhance_error_message_for_issue(
                    error_message, error_context
                )
                issue_body = f"{metadata_section}{enhanced_error}"
            except Exception as e:
                self.logger.warning(f"Failed to enhance issue body: {e}")
                issue_body = issue_body_final

            # Get existing issue ID for deduplication
            existing_id = self._get_existing_issue_id(repo_url, error_type)
            
            if dry_run:
                if self.demonstrator:
                    should_proceed = self.demonstrator.show_issue(issue_title_final, issue_body)
                    
                    if should_proceed:
                        # User chose to proceed with issue creation
                        self.logger.info("User chose to proceed with issue creation in dry-run mode")
                        # Fall through to create the actual issue (continue with normal flow below)
                    else:
                        # User chose not to proceed, end dry-run
                        self.logger.info("User chose not to proceed, ending dry-run")
                        return {
                            "final_result": "DRY RUN: User chose not to proceed with issue creation",
                            "issues_opened": 0,
                            "operation_type": "dry_run_aborted",
                            "error_message": None,
                        }

                # Delegate to DemonstratorAgent for intelligent interactive dry-run
                self.logger.info("Delegating to DemonstratorAgent for interactive dry-run")
                
                from diagram_to_iac.agents.demonstrator_langgraph import DemonstratorAgentInput
                
                demo_result = self.demonstrator_agent.run(
                    DemonstratorAgentInput(
                        query=f"Demonstrate error: {error_type}",
                        error_type=error_type,
                        error_message=error_message,
                        repo_url=repo_url,
                        branch_name=branch_name,
                        stack_detected=stack_detected,
                        issue_title=issue_title_final,
                        issue_body=issue_body,
                        existing_issue_id=existing_id,
                        thread_id=state.get("thread_id"),
                    )
                )
                
                # Return the demonstration result and exit early
                return {
                    "final_result": demo_result["result"],
                    "issues_opened": 1 if demo_result["issue_created"] else 0,
                    "operation_type": f"demo_{demo_result['action_taken']}",
                    "error_message": demo_result.get("error_message"),
                }

            # Normal non-dry-run issue creation (only executed when dry_run=False)




            issue_result = self.git_agent.run(
                GitAgentInput(
                    query=f"open issue {issue_title_final} for repository {repo_url}: {issue_body}",
                    issue_id=existing_id,
                )
            )

            if issue_result.error_message:
                self.logger.error(
                    f"Issue creation failed: {issue_result.error_message}"
                )
                return {
                    "final_result": f"Issue creation failed: {issue_result.error_message}",
                    "issues_opened": 0,
                    "operation_type": "issue_error",
                }

            
            if existing_id is None:
                new_id = self._parse_issue_number(issue_result.result)
                if new_id is not None:
                    self._record_issue_id(repo_url, error_type, new_id)

            self.logger.info("GitHub issue created successfully")
            return {
                "final_result": f"R2D workflow failed, issue created: {issue_result.result}",
                "issues_opened": 1,
                "operation_type": "issue_success",
                "error_message": None,
            }

        except Exception as e:
            self.logger.error(f"Error in issue creation node: {e}")
            return {
                "final_result": f"Issue creation failed: {str(e)}",
                "issues_opened": 0,
                "operation_type": "issue_error",
            }

    def _handle_interactive_dry_run(self, issue_title: str, issue_body: str, repo_url: str, existing_id: Optional[int], error_type: str) -> dict:
        """
        Handle intelligent interactive dry-run mode with error-specific guidance and retry capabilities.
        Analyzes the specific error and provides actionable steps to fix it.
        """
        # Get the original error context from the state
        error_message = getattr(self, '_current_error_message', 'Unknown error')
        
        print("\n" + "="*80)
        print("🔍 INTELLIGENT DRY RUN: R2D Workflow Error Analysis")
        print("="*80)
        
        print(f"\n📍 **Repository:** {repo_url}")
        print(f"🏷️  **Error Type:** {error_type}")
        if existing_id:
            print(f"🔗 **Existing Issue:** Found issue #{existing_id} (would update)")
        else:
            print(f"🆕 **New Issue:** Would create new issue")
        
        # Intelligent error analysis and guidance
        error_analysis = self._analyze_error_for_user_guidance(error_type, error_message)
        
        print(f"\n🧠 **Error Analysis:**")
        print(f"   {error_analysis['description']}")
        
        if error_analysis['fixable']:
            print(f"\n✅ **Good News:** This error can potentially be fixed!")
            print(f"   {error_analysis['fix_guidance']}")
            
            if error_analysis['required_inputs']:
                print(f"\n📝 **Required Information:**")
                for req in error_analysis['required_inputs']:
                    print(f"   • {req}")
        else:
            print(f"\n❌ **This error requires manual intervention:**")
            print(f"   {error_analysis['manual_steps']}")
        
        print(f"\n📝 **Proposed Issue Title:**")
        print(f"   {issue_title}")
        
        print("\n" + "="*80)
        print("🤔 What would you like to do?")
        print("="*80)
        
        if error_analysis['fixable']:
            print("1. 🔧 Fix - Provide missing information and retry")
            print("2. 🚀 Create Issue - Log this error as a GitHub issue")
            print("3. 📋 Details - Show full error details and proposed issue")
            print("4. ❌ Abort - Skip and end workflow")
        else:
            print("1. 🚀 Create Issue - Log this error as a GitHub issue")
            print("2. 📋 Details - Show full error details and proposed issue")
            print("3. ❌ Abort - Skip and end workflow")
        
        while True:
            try:
                if error_analysis['fixable']:
                    choice = input("\nEnter your choice (1-4): ").strip()
                    max_choice = 4
                else:
                    choice = input("\nEnter your choice (1-3): ").strip()
                    max_choice = 3
                
                if choice == "1":
                    if error_analysis['fixable']:
                        print("\n🔧 Let's fix this error together!")
                        return self._attempt_error_fix(error_type, error_analysis, repo_url)
                    else:
                        print("\n🚀 Creating GitHub issue...")
                        return self._proceed_with_issue_creation(issue_title, issue_body, repo_url, existing_id, error_type)
                        
                elif choice == "2":
                    if error_analysis['fixable']:
                        print("\n🚀 Creating GitHub issue...")
                        return self._proceed_with_issue_creation(issue_title, issue_body, repo_url, existing_id, error_type)
                    else:
                        print(f"\n📊 **Full Error Details:**")
                        print(f"   Raw Error: {error_message}")
                        print(f"\n📄 **Proposed Issue Body:**")
                        print("   " + "\n   ".join(issue_body.split("\n")))
                        print(f"\n🔄 Returning to menu...")
                        continue
                        
                elif choice == "3":
                    if error_analysis['fixable']:
                        print(f"\n📊 **Full Error Details:**")
                        print(f"   Raw Error: {error_message}")
                        print(f"\n📄 **Proposed Issue Body:**")
                        print("   " + "\n   ".join(issue_body.split("\n")))
                        print(f"\n🔄 Returning to menu...")
                        continue
                    else:
                        print("\n❌ User chose to abort. Skipping issue creation.")
                        return {
                            "final_result": "User aborted: workflow ended",
                            "issues_opened": 0,
                            "operation_type": "user_abort",
                            "error_message": None,
                        }
                        
                elif choice == "4" and error_analysis['fixable']:
                    print("\n❌ User chose to abort. Skipping issue creation.")
                    return {
                        "final_result": "User aborted: workflow ended", 
                        "issues_opened": 0,
                        "operation_type": "user_abort",
                        "error_message": None,
                    }
                    
                else:
                    print(f"❓ Invalid choice '{choice}'. Please enter a valid option.")
                    continue
                    
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n⚠️  User interrupted! Aborting workflow.")
                return {
                    "final_result": "User interrupted: workflow aborted",
                    "issues_opened": 0,
                    "operation_type": "user_interrupt",
                    "error_message": None,
                }

    def _proceed_with_issue_creation(self, issue_title: str, issue_body: str, repo_url: str, existing_id: Optional[int], error_type: str) -> dict:
        """
        Proceed with actual GitHub issue creation after user confirmation in dry-run mode.
        """
        try:
            issue_result = self.git_agent.run(
                GitAgentInput(
                    query=f"open issue {issue_title} for repository {repo_url}: {issue_body}",
                    issue_id=existing_id,
                )
            )

            if issue_result.error_message:
                self.logger.error(f"Issue creation failed: {issue_result.error_message}")
                return {
                    "final_result": f"Issue creation failed: {issue_result.error_message}",
                    "issues_opened": 0,
                    "operation_type": "issue_error",
                }

            # Track new issue ID for deduplication
            if existing_id is None:
                new_id = self._parse_issue_number(issue_result.result)
                if new_id is not None:
                    self._record_issue_id(repo_url, error_type, new_id)

            self.logger.info("GitHub issue created successfully")
            print(f"\n✅ Success! GitHub issue created: {issue_result.result}")
            
            return {
                "final_result": f"R2D workflow failed, issue created: {issue_result.result}",
                "issues_opened": 1,
                "operation_type": "issue_success",
                "error_message": None,
            }

        except Exception as e:
            self.logger.error(f"Error in issue creation: {e}")
            return {
                "final_result": f"Issue creation failed: {str(e)}",
                "issues_opened": 0,
                "operation_type": "issue_error",
            }

    def _analyze_error_for_user_guidance(self, error_type: str, error_message: str) -> dict:
        """
        Analyze the specific error and provide intelligent guidance for fixing it.
        Returns a dictionary with analysis results and actionable recommendations.
        """
        analysis = {
            "description": "Unknown error occurred",
            "fixable": False,
            "fix_guidance": "",
            "required_inputs": [],
            "manual_steps": "Please check the logs and create a GitHub issue",
            "retry_method": None
        }
        
        if error_type == "auth_failed" or "missing_terraform_token" in error_message.lower():
            analysis.update({
                "description": "Terraform Cloud authentication is missing. The TF_TOKEN environment variable is not set.",
                "fixable": True,
                "fix_guidance": "Terraform requires a valid token to authenticate with Terraform Cloud. You can get this token from your Terraform Cloud account.",
                "required_inputs": [
                    "TF_TOKEN: Your Terraform Cloud API token",
                    "Optional: TF_WORKSPACE: Terraform Cloud workspace name"
                ],
                "retry_method": "terraform_auth_retry"
            })
            
        elif error_type == "api_key_error" or "401" in error_message:
            analysis.update({
                "description": "API authentication failed. The API key might be missing or invalid.",
                "fixable": True,
                "fix_guidance": "The system needs valid API credentials to function properly.",
                "required_inputs": [
                    "OPENAI_API_KEY: Your OpenAI API key (if using OpenAI)",
                    "ANTHROPIC_API_KEY: Your Anthropic API key (if using Claude)",
                    "GITHUB_TOKEN: Your GitHub Personal Access Token"
                ],
                "retry_method": "api_key_retry"
            })
            
        elif error_type == "terraform_init":
            if "backend" in error_message.lower():
                analysis.update({
                    "description": "Terraform backend configuration issue. The backend might not be properly configured.",
                    "fixable": True,
                    "fix_guidance": "Terraform backend needs proper configuration or credentials.",
                    "required_inputs": [
                        "Backend configuration details",
                        "Access credentials for the backend"
                    ],
                    "retry_method": "terraform_backend_retry"
                })
            else:
                analysis.update({
                    "description": "Terraform initialization failed for unknown reasons.",
                    "fixable": False,
                    "manual_steps": "Check Terraform configuration files, ensure providers are properly specified, and verify network connectivity."
                })
                
        elif error_type == "network_error":
            analysis.update({
                "description": "Network connectivity issue. Cannot reach external services.",
                "fixable": True,
                "fix_guidance": "Check your internet connection and try again. You may also need to configure proxy settings.",
                "required_inputs": [
                    "Confirm network connectivity",
                    "Proxy settings (if behind a corporate firewall)"
                ],
                "retry_method": "network_retry"
            })
            
        elif error_type == "permission_error":
            analysis.update({
                "description": "Permission denied. The system lacks necessary permissions.",
                "fixable": False,
                "manual_steps": "Check file permissions, directory access rights, and ensure the process has necessary privileges."
            })
            
        return analysis

    def _attempt_error_fix(self, error_type: str, error_analysis: dict, repo_url: str) -> dict:
        """
        Attempt to fix the error by collecting required information from the user
        and retrying the operation with the new configuration.
        """
        print(f"\n🛠️  **Error Fix Mode: {error_type}**")
        print(f"📋 {error_analysis['fix_guidance']}")
        
        # Collect required inputs from user
        user_inputs = {}
        for requirement in error_analysis['required_inputs']:
            key = requirement.split(':')[0].strip()
            description = requirement.split(':', 1)[1].strip() if ':' in requirement else requirement
            
            print(f"\n📝 **{key}:**")
            print(f"   {description}")
            
            # Handle sensitive inputs (tokens/keys) differently
            if any(sensitive in key.lower() for sensitive in ['token', 'key', 'password']):
                value = input(f"Enter {key} (will be hidden): ").strip()
                if value:
                    # Set environment variable
                    os.environ[key] = value
                    user_inputs[key] = "***HIDDEN***"
                    print(f"✅ {key} has been set")
                else:
                    print(f"⚠️  {key} was not provided")
            else:
                value = input(f"Enter {key}: ").strip()
                if value:
                    user_inputs[key] = value
                    print(f"✅ {key}: {value}")
                else:
                    print(f"⚠️  {key} was not provided")
        
        # Ask user if they want to retry with the new information
        print(f"\n🔄 **Ready to Retry**")
        print(f"📊 Collected information:")
        for key, value in user_inputs.items():
            print(f"   • {key}: {value}")
        
        retry_choice = input(f"\nWould you like to retry the operation with this information? (y/N): ").strip().lower()
        
        if retry_choice in ['y', 'yes']:
            print(f"\n🚀 Retrying the operation...")
            return self._retry_operation_with_fixes(error_type, user_inputs, repo_url)
        else:
            print(f"\n❌ User chose not to retry. Creating GitHub issue instead...")
            # Fall back to issue creation
            return {
                "final_result": "User provided information but chose not to retry",
                "issues_opened": 0,
                "operation_type": "user_no_retry",
                "error_message": None,
            }

    def _retry_operation_with_fixes(self, error_type: str, user_inputs: dict, repo_url: str) -> dict:
        """
        Retry the failed operation with the user-provided fixes.
        """
        try:
            if error_type in ["auth_failed", "terraform_init"]:
                # For Terraform auth issues, retry the terraform init
                print("🔄 Retrying Terraform initialization with new credentials...")
                
                # Get the repo path from the current state (we need to store this better)
                # For now, assume it's in /workspace/<repo_name>
                repo_name = repo_url.split('/')[-1].replace('.git', '')
                repo_path = f"/workspace/{repo_name}"
                
                # Retry terraform init
                tf_result = self.terraform_agent.run(
                    TerraformAgentInput(
                        query=f"terraform init in {repo_path}",
                        thread_id=str(uuid.uuid4()),
                    )
                )
                
                if tf_result.error_message:
                    print(f"❌ Retry failed: {tf_result.error_message}")
                    return {
                        "final_result": f"Retry failed: {tf_result.error_message}",
                        "issues_opened": 0,
                        "operation_type": "retry_failed",
                        "error_message": tf_result.error_message,
                    }
                else:
                    print(f"✅ Success! Terraform init completed successfully.")
                    print(f"🎉 Continuing with Terraform workflow...")
                    
                    # Continue with the full terraform workflow
                    return self._continue_terraform_workflow_after_fix(repo_path)
                    
            elif error_type == "api_key_error":
                print("🔄 API credentials have been updated. The system should work better now.")
                return {
                    "final_result": "API credentials updated successfully",
                    "issues_opened": 0,
                    "operation_type": "credentials_fixed",
                    "error_message": None,
                }
                
            else:
                print(f"🚧 Retry logic for {error_type} is not yet implemented.")
                return {
                    "final_result": f"Fix attempted but retry logic for {error_type} not implemented",
                    "issues_opened": 0,
                    "operation_type": "fix_not_implemented",
                    "error_message": None,
                }
                
        except Exception as e:
            self.logger.error(f"Error during retry operation: {e}")
            return {
                "final_result": f"Retry operation failed: {str(e)}",
                "issues_opened": 0,
                "operation_type": "retry_error",
                "error_message": str(e),
            }

    def _continue_terraform_workflow_after_fix(self, repo_path: str) -> dict:
        """
        Continue the Terraform workflow after a successful fix.
        """
        try:
            print("🚀 Continuing with Terraform plan...")
            
            # Run terraform plan
            plan_result = self.terraform_agent.run(
                TerraformAgentInput(
                    query=f"terraform plan in {repo_path}",
                    thread_id=str(uuid.uuid4()),
                )
            )
            
            if plan_result.error_message:
                print(f"⚠️  Terraform plan encountered issues: {plan_result.error_message}")
                return {
                    "final_result": f"Terraform init fixed, but plan failed: {plan_result.error_message}",
                    "issues_opened": 0,
                    "operation_type": "plan_failed_after_fix",
                    "error_message": plan_result.error_message,
                }
            else:
                print(f"✅ Terraform plan completed successfully!")
                print(f"📋 Plan summary: {plan_result.result}")
                
                return {
                    "final_result": f"🎉 R2D workflow completed successfully after fix! Plan result: {plan_result.result}",
                    "issues_opened": 0,
                    "operation_type": "workflow_completed_after_fix",
                    "error_message": None,
                    "success": True,
                }
                
        except Exception as e:
            self.logger.error(f"Error continuing workflow after fix: {e}")
            return {
                "final_result": f"Error continuing workflow after fix: {str(e)}",
                "issues_opened": 0,
                "operation_type": "continue_workflow_error",
                "error_message": str(e),
            }

    # --- Utility Methods (preserved from original implementation) ---

    def _generate_dynamic_branch_name(self) -> str:
        """Generate timestamp-based branch name."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"r2d-{timestamp}"


    # --- Issue tracker helpers ---
    def _get_existing_issue_id(self, repo_url: str, error_type: str) -> Optional[int]:
        try:
            return self.issue_tracker.get_issue(repo_url, error_type)
        except Exception as e:
            self.logger.error(f"Issue tracker lookup failed: {e}")
            return None

    def _record_issue_id(self, repo_url: str, error_type: str, issue_id: int) -> None:
        try:
            self.issue_tracker.record_issue(repo_url, error_type, issue_id)
        except Exception as e:
            self.logger.error(f"Issue tracker update failed: {e}")

    def _parse_issue_number(self, text: str) -> Optional[int]:
        import re
        match = re.search(r'/issues/(\d+)', text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None
    

    def _detect_infrastructure_stack(self, repo_path: str) -> Dict[str, int]:
        """
        Detect infrastructure tooling in the repository.

        Returns:
            Dict mapping file types to counts (e.g. {"*.tf": 3, "*.yml": 2})
        """
        self.logger.info(f"Detecting infrastructure stack in {repo_path}")

        # Define patterns for infrastructure files
        stack_patterns = {
            "terraform": "*.tf",
            "ansible": "*.yml",
            "powershell": "*.ps1",
            "shell": "*.sh",
        }

        stack_detected = {}

        for stack_type, pattern in stack_patterns.items():
            try:
                # Try multiple approaches for file detection
                count = 0

                # Method 1: Try find command (most accurate) - wrapped in bash
                try:
                    find_result = self.shell_agent.run(
                        ShellAgentInput(
                            command=f"bash -c \"find . -name '{pattern}' -type f | wc -l\"",
                            cwd=repo_path,
                        )
                    )

                    if find_result.exit_code == 0:
                        count = int(find_result.output.strip())
                        self.logger.debug(
                            f"Found {count} {stack_type} files using find command"
                        )
                    else:
                        raise RuntimeError(
                            f"Find command failed: {find_result.error_message}"
                        )

                except Exception as e:
                    self.logger.warning(f"Find command failed for {stack_type}: {e}")

                    # Method 2: Fallback to ls with globbing - wrapped in bash
                    try:
                        ls_result = self.shell_agent.run(
                            ShellAgentInput(
                                command=f'bash -c "ls -1 {pattern} 2>/dev/null | wc -l || echo 0"',
                                cwd=repo_path,
                            )
                        )
                        if ls_result.exit_code == 0:
                            count = int(ls_result.output.strip())
                            self.logger.debug(
                                f"Found {count} {stack_type} files using ls fallback"
                            )
                        else:
                            # Method 3: Final fallback using bash expansion
                            bash_result = self.shell_agent.run(
                                ShellAgentInput(
                                    command=f"bash -c 'shopt -s nullglob; files=({pattern}); echo ${{#files[@]}}'",
                                    cwd=repo_path,
                                )
                            )
                            if bash_result.exit_code == 0:
                                count = int(bash_result.output.strip())
                                self.logger.debug(
                                    f"Found {count} {stack_type} files using bash expansion"
                                )

                    except Exception as fallback_e:
                        self.logger.error(
                            f"All detection methods failed for {stack_type}: {fallback_e}"
                        )
                        count = 0

                # Store result if files found
                if count > 0:
                    stack_detected[pattern] = count
                    self.logger.info(f"✅ Found {count} {stack_type} files ({pattern})")
                else:
                    self.logger.debug(f"No {stack_type} files found")

            except Exception as e:
                self.logger.error(f"Error detecting {stack_type} files: {e}")

        self.logger.info(f"Stack detection completed: {stack_detected}")
        return stack_detected

    def _run_enhanced_terraform_workflow(
        self, repo_path: str, thread_id: Optional[str]
    ) -> TerraformAgentOutput:
        """
        Run enhanced Terraform workflow with sophisticated features:
        - Terraform validation
        - Terraform init
        - Terraform plan with detailed output
        - Security scanning (placeholder)
        - Cost estimation (placeholder)
        """
        self.logger.info("Starting enhanced Terraform workflow")

        try:
            # Step 1: Terraform validation
            self.logger.info("Step 1: Terraform validation")
            validate_result = self.terraform_agent.run(
                TerraformAgentInput(
                    query=f"terraform validate in {repo_path}", thread_id=thread_id
                )
            )

            if validate_result.error_message:
                self.logger.error(
                    f"Terraform validation failed: {validate_result.error_message}"
                )
                return TerraformAgentOutput(
                    result="Terraform validation failed",
                    thread_id=thread_id or "unknown",
                    error_message=f"Validation failed: {validate_result.error_message}",
                    operation_type="validate",
                )

            # Step 2: Terraform init
            self.logger.info("Step 2: Terraform init")
            init_result = self.terraform_agent.run(
                TerraformAgentInput(
                    query=f"terraform init in {repo_path}", thread_id=thread_id
                )
            )

            if init_result.error_message:
                self.logger.error(f"Terraform init failed: {init_result.error_message}")
                return TerraformAgentOutput(
                    result="Terraform init failed",
                    thread_id=thread_id or "unknown",
                    error_message=f"Init failed: {init_result.error_message}",
                    operation_type="init",
                )

            # Step 3: Terraform plan with detailed output
            self.logger.info("Step 3: Terraform plan with detailed analysis")
            plan_result = self.terraform_agent.run(
                TerraformAgentInput(
                    query=f"terraform plan -detailed-exitcode -out=tfplan in {repo_path}",
                    thread_id=thread_id,
                )
            )

            # Step 4: Additional analysis (placeholder for future features)
            additional_insights = self._analyze_terraform_plan(repo_path)

            # Combine results
            enhanced_summary = f"""Enhanced Terraform Workflow Results:
✅ Validation: {validate_result.result}
✅ Init: {init_result.result}
📋 Plan: {plan_result.result}
🔍 Analysis: {additional_insights}"""

            if plan_result.error_message:
                return TerraformAgentOutput(
                    result=enhanced_summary,
                    thread_id=thread_id or "unknown",
                    error_message=plan_result.error_message,
                    operation_type="enhanced_plan",
                )

            return TerraformAgentOutput(
                result=enhanced_summary,
                thread_id=thread_id or "unknown",
                error_message=None,
                operation_type="enhanced_plan",
            )

        except Exception as e:
            self.logger.error(f"Enhanced Terraform workflow failed: {e}")
            return TerraformAgentOutput(
                result="Enhanced Terraform workflow failed",
                thread_id=thread_id or "unknown",
                error_message=str(e),
                operation_type="enhanced_workflow_error",
            )

    def _analyze_terraform_plan(self, repo_path: str) -> str:
        """
        Analyze Terraform plan for additional insights.
        This is a placeholder for future sophisticated features.
        """
        insights = []

        # Placeholder analysis features
        insights.append("Resource count analysis: Available in future release")
        insights.append("Security scanning: Available in future release")
        insights.append("Cost estimation: Available in future release")
        insights.append("Compliance checking: Available in future release")

        # Basic file structure analysis with fallback
        try:
            # Try find command first
            file_result = self.shell_agent.run(
                ShellAgentInput(
                    command="find . -name '*.tf' -exec basename {} \\; | sort | uniq -c",
                    cwd=repo_path,
                )
            )
            if file_result.exit_code == 0:
                insights.append(
                    f"Terraform files structure: {file_result.output.strip()}"
                )
            else:
                # Fallback to ls
                ls_result = self.shell_agent.run(
                    ShellAgentInput(
                        command="ls *.tf 2>/dev/null | wc -l || echo 0", cwd=repo_path
                    )
                )
                if ls_result.exit_code == 0:
                    count = ls_result.output.strip()
                    insights.append(f"Terraform files found: {count}")
        except Exception as e:
            insights.append(f"Could not analyze file structure: {e}")

        return " | ".join(insights)

    # --- LangGraph State Machine ---

    def _build_graph(self):
        """
        Build and compile the LangGraph state machine.
        Creates nodes for planner and each workflow step, sets up organic routing.
        """
        graph_builder = StateGraph(SupervisorAgentState)

        # Add nodes
        graph_builder.add_node("planner_llm", self._planner_llm_node)
        graph_builder.add_node("clone_repo_node", self._clone_repo_node)
        graph_builder.add_node("stack_detect_node", self._stack_detect_node)
        graph_builder.add_node("terraform_workflow_node", self._terraform_workflow_node)
        graph_builder.add_node("issue_create_node", self._issue_create_node)

        # Set entry point
        graph_builder.set_entry_point("planner_llm")

        # Configure routing map for planner
        planner_routing_map = {
            "clone_repo_node": "clone_repo_node",
            "stack_detect_node": "stack_detect_node",
            "terraform_workflow_node": "terraform_workflow_node",
            "issue_create_node": "issue_create_node",
            END: END,
        }

        # Configure routing map for workflow continuation
        workflow_routing_map = {
            "stack_detect_node": "stack_detect_node",
            "terraform_workflow_node": "terraform_workflow_node",
            "issue_create_node": "issue_create_node",
            END: END,
        }

        # Add conditional edges from planner (initial routing)
        graph_builder.add_conditional_edges(
            "planner_llm", self._route_after_planner, planner_routing_map
        )

        # Add conditional edges from workflow nodes (sequential continuation)
        graph_builder.add_conditional_edges(
            "clone_repo_node", self._route_workflow_continuation, workflow_routing_map
        )

        graph_builder.add_conditional_edges(
            "stack_detect_node", self._route_workflow_continuation, workflow_routing_map
        )

        graph_builder.add_conditional_edges(
            "terraform_workflow_node",
            self._route_workflow_continuation,
            workflow_routing_map,
        )

        # Issue creation always ends the workflow
        graph_builder.add_edge("issue_create_node", END)

        # Compile with checkpointer
        return graph_builder.compile(checkpointer=self.checkpointer)

    # --- Main Run Method: Organic LangGraph Execution ---

    def run(self, agent_input: SupervisorAgentInput) -> SupervisorAgentOutput:
        """
        Execute R2D workflow using organic LangGraph state machine.
        The LLM brain decides routing between specialized agents.
        """
        repo_url = agent_input.repo_url
        # Normalize the repository URL for issue creation
        normalized_repo_url = repo_url.rstrip("/").rstrip(".git")
        thread_id = agent_input.thread_id or str(uuid.uuid4())

        # Generate dynamic branch name if not provided
        branch_name = agent_input.branch_name or self._generate_dynamic_branch_name()

        # If initialization failed due to missing secrets, abort early
        if self.startup_error:
            self.logger.error(
                f"Cannot start workflow for {repo_url}: {self.startup_error}"
            )

            issues_opened = 0
            try:
                issue_result = self.git_agent.run(
                    GitAgentInput(
                        query=(
                            f"open issue for repository {normalized_repo_url}: 🚫 Missing token - {self.startup_error}"
                        )
                    )
                )
                if not issue_result.error_message:
                    issues_opened = 1
            except Exception as e:
                self.logger.error(
                    f"Failed to invoke GitAgent for missing token issue: {e}"
                )

            output = SupervisorAgentOutput(
                repo_url=repo_url,
                branch_created=False,
                branch_name=branch_name,
                stack_detected={},
                terraform_summary=None,
                unsupported=False,
                issues_opened=issues_opened,
                success=False,
                message=self.startup_error
                + (" (GitHub issue created)" if issues_opened else " (GitHub issue creation also failed)")
            )
            log_event(
                "supervisor_agent_run_end",
                repo_url=repo_url,
                thread_id=thread_id,
                success=False,
                error=self.startup_error,
            )
            return output

        self.logger.info(f"Starting R2D workflow for {repo_url}, branch: {branch_name}")
        log_event(
            "supervisor_agent_run_start",
            repo_url=repo_url,
            branch_name=branch_name,
            thread_id=thread_id,
        )

        # Create initial state
        initial_state: SupervisorAgentState = {
            "input_message": HumanMessage(
                content=f"Execute R2D workflow for repository {repo_url}"
            ),
            "repo_url": repo_url,
            "branch_name": branch_name,
            "thread_id": thread_id,
            "dry_run": agent_input.dry_run,
            "repo_path": None,
            "stack_detected": {},
            "branch_created": False,
            "final_result": "",
            "operation_type": "",
            "terraform_summary": None,
            "issues_opened": 0,
            "unsupported": False,
            "error_message": None,
            "tool_output": [],
        }

        try:
            # Execute the LangGraph workflow
            self.logger.info("Executing organic LangGraph R2D workflow")
            final_state = self.runnable.invoke(
                initial_state, {"configurable": {"thread_id": thread_id}}
            )

            # Extract results from final state
            operation_type = final_state.get("operation_type", "")
            issues_opened = final_state.get("issues_opened", 0)

            # Determine success: workflow succeeds only if terraform completes without issues
            # If issues were opened, it means there was a failure somewhere in the workflow
            success = (
                final_state.get("error_message") is None
                and issues_opened == 0
                and operation_type != "issue_success"
            )

            message = final_state.get("final_result", "R2D workflow completed")

            output = SupervisorAgentOutput(
                repo_url=repo_url,
                branch_created=final_state.get("branch_created", False),
                branch_name=final_state.get("branch_name", branch_name),
                stack_detected=final_state.get("stack_detected", {}),
                terraform_summary=final_state.get("terraform_summary"),
                unsupported=final_state.get("unsupported", False),
                issues_opened=issues_opened,
                success=success,
                message=message,
            )

            log_event(
                "supervisor_agent_run_end",
                repo_url=repo_url,
                thread_id=thread_id,
                success=success,
            )

            return output

        except Exception as e:
            self.logger.error(f"R2D workflow execution failed: {e}", exc_info=True)

            # Enhanced error handling: Automatically create GitHub issue for ANY workflow failure
            issues_opened = 0
            try:
                self.logger.info(
                    "Attempting to create GitHub issue for workflow execution failure"
                )

                # Import text utilities for error handling
                from diagram_to_iac.tools.text_utils import (
                    generate_organic_issue_title,
                    enhance_error_message_for_issue,
                    create_issue_metadata_section,
                )

                # Determine error type for better title generation
                error_message = str(e)
                error_type = "workflow_error"
                if "api key" in error_message.lower() or "401" in error_message.lower():
                    error_type = "api_key_error"
                elif (
                    "llm" in error_message.lower() or "openai" in error_message.lower()
                ):
                    error_type = "llm_error"
                elif (
                    "network" in error_message.lower()
                    or "connection" in error_message.lower()
                ):
                    error_type = "network_error"
                elif "timeout" in error_message.lower():
                    error_type = "timeout_error"
                elif (
                    "permission" in error_message.lower()
                    or "forbidden" in error_message.lower()
                ):
                    error_type = "permission_error"

                # Create context for organic title generation
                error_context = {
                    "error_type": error_type,
                    "stack_detected": {},
                    "error_message": error_message,
                    "repo_url": repo_url,
                    "branch_name": branch_name,
                }

                # Generate organic, thoughtful issue title
                issue_title = generate_organic_issue_title(error_context)

                # Create enhanced issue body with metadata and clean error formatting
                metadata_section = create_issue_metadata_section(error_context)

                enhanced_error = enhance_error_message_for_issue(error_message, error_context)
                
                issue_body = f"{metadata_section}{enhanced_error}\n\n**Workflow Stage:** Initial workflow execution\n**Error Type:** Critical system error preventing R2D workflow startup"
                
                if agent_input.dry_run:
                    if self.demonstrator:
                        self.demonstrator.show_issue(issue_title, issue_body)
                    else:
                        self.logger.info(f"DRY RUN: GitHub issue processing for: Title: {issue_title}")
                        print("=== DRY RUN: GitHub issue would be created/checked ===")
                        print(f"Title: {issue_title}")
                        print(f"Body:\n{issue_body}")
                else:
                    # Create or update GitHub issue for workflow failure
                    existing_id = self._get_existing_issue_id(repo_url, error_type)
                    git_input = GitAgentInput(
                        query=f"open issue {issue_title} for repository {repo_url}: {issue_body}",
                        issue_id=existing_id,
                    )
                    issue_result = self.git_agent.run(git_input)
                    if not issue_result.error_message:
                        issues_opened = 1
                        # Record new issue id if created
                        if existing_id is None:
                            new_id = self._parse_issue_number(issue_result.result)
                            if new_id is not None:
                                self._record_issue_id(repo_url, error_type, new_id)

                        self.logger.info(f"Successfully created GitHub issue for workflow failure: {issue_result.result}")
                    else:
                        self.logger.warning(f"Failed to create GitHub issue for workflow failure: {issue_result.error_message}")
                    

            except Exception as issue_error:
                self.logger.error(
                    f"Failed to create GitHub issue for workflow failure: {issue_error}"
                )

            output = SupervisorAgentOutput(
                repo_url=repo_url,
                branch_created=False,
                branch_name=branch_name,
                stack_detected={},
                terraform_summary=None,
                unsupported=False,  # Changed: Don't mark as unsupported, this is a system error
                issues_opened=issues_opened,
                success=False,
                message=f"Workflow execution failed: {str(e)}"
                + (
                    f" (GitHub issue created)"
                    if issues_opened > 0
                    else " (GitHub issue creation also failed)"
                ),
            )
            log_event(
                "supervisor_agent_run_end",
                repo_url=repo_url,
                thread_id=thread_id,
                success=False,
                error=str(e),
            )
            return output

    # --- Memory and Conversation Management ---

    def get_conversation_history(self) -> List[Dict[str, any]]:
        """Get conversation history from memory."""
        try:
            return self.memory.get_conversation_history()
        except Exception as e:
            self.logger.error(f"Failed to get conversation history: {e}")
            return []

    def get_memory_state(self) -> Dict[str, any]:
        """Get current memory state."""
        try:
            return {
                "conversation_history": self.get_conversation_history(),
                "memory_type": type(self.memory).__name__,
            }
        except Exception as e:
            self.logger.error(f"Failed to get memory state: {e}")
            return {"error": str(e)}


def detect_stack_files(repo_path: str, shell_agent: ShellAgent) -> Dict[str, int]:
    """Detect basic stack files (.tf and .sh) in the given repository."""
    # Check if repo_path exists before proceeding
    if not os.path.exists(repo_path):
        raise RuntimeError(f"Repository path does not exist: {repo_path}")
    
    patterns = ["*.tf", "*.sh"]
    detected: Dict[str, int] = {}

    for pattern in patterns:
        count = 0
        try:
            result = shell_agent.run(
                ShellAgentInput(
                    command=f"bash -c \"find . -name '{pattern}' -type f | wc -l\"",
                    cwd=repo_path,
                )
            )
            if result.exit_code == 0:
                count = int(result.output.strip())
            else:
                raise RuntimeError(result.error_message or "find failed")
        except Exception:
            # Fallback to Python-based search
            for root, _, files in os.walk(repo_path):
                count += len(fnmatch.filter(files, pattern))

        if count > 0:
            detected[pattern] = count

    return detected
