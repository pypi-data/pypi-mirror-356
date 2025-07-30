"""MLflow-based tracer for Langflow integration."""

import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID

import mlflow

# MLflow 3.1.0+ uses different tracing API
MLFLOW_TRACING_AVAILABLE = True

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

from ..core.mlflow_client import MLflowClient
from ..utils.logger import setup_logger
from ..monitoring.cost_tracking import CostTracker

logger = setup_logger(__name__)


class MLflowLangChainCallback(BaseCallbackHandler):
    """LangChain callback handler for MLflow tracing."""

    def __init__(self, tracer):
        super().__init__()
        self.tracer = tracer
        self.llm_runs = {}
        self.cost_tracker = CostTracker()

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs
    ) -> None:
        """Start LLM run tracking."""
        logger.debug("LLM callback: on_llm_start called")

        # Check if we have an active MLflow run
        try:
            if hasattr(self.tracer, "_mlflow") and self.tracer._mlflow:
                active_run = self.tracer._mlflow.active_run()
                if active_run:
                    logger.debug(
                        f"Active MLflow run: {active_run.info.run_name} (ID: {active_run.info.run_id})"
                    )
                else:
                    logger.debug("No active MLflow run during callback")
            else:
                logger.debug("No MLflow instance available in tracer")
        except Exception as e:
            logger.debug(f"Error checking active run: {e}")

        run_id = str(kwargs.get("run_id", ""))
        if not run_id:
            return

        model_name = "unknown"

        # Debug logging
        logger.debug(f"on_llm_start called with serialized: {serialized}")
        logger.debug(f"on_llm_start kwargs: {kwargs}")

        # Extract model name from serialized info
        if "id" in serialized and isinstance(serialized["id"], list):
            model_name = serialized["id"][-1]

        # If we get a generic name like "ChatOpenAI", try to get the actual model
        if model_name in [
            "ChatOpenAI",
            "chatopenai",
            "azurechatopenai",
            "chatanthropic",
            "chatbedrock",
        ]:
            # Try to get from invocation_params
            invocation_params = kwargs.get("invocation_params", {})
            logger.debug(f"invocation_params: {invocation_params}")

            # Check various model parameter names
            model_params = ["model", "model_name", "model_id", "deployment_name"]
            for param in model_params:
                if param in invocation_params and invocation_params[param]:
                    model_name = invocation_params[param]
                    logger.debug(
                        f"Found model name '{model_name}' in invocation_params['{param}']"
                    )
                    break

        self.llm_runs[run_id] = {
            "start_time": time.time(),
            "prompts": prompts,
            "model": model_name,
            "invocation_params": kwargs.get("invocation_params", {}),
        }

        logger.debug(f"Started LLM run {run_id} with model {model_name}")

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """End LLM run and track costs."""
        logger.debug("LLM callback: on_llm_end called")

        # Check if we have an active MLflow run
        try:
            if hasattr(self.tracer, "_mlflow") and self.tracer._mlflow:
                active_run = self.tracer._mlflow.active_run()
                if active_run:
                    logger.debug(
                        f"Active MLflow run during on_llm_end: {active_run.info.run_name} (ID: {active_run.info.run_id})"
                    )
                else:
                    logger.debug("No active MLflow run during on_llm_end")
            else:
                logger.debug("No MLflow instance available in tracer during on_llm_end")
        except Exception as e:
            logger.debug(f"Error checking active run during on_llm_end: {e}")

        run_id = str(kwargs.get("run_id", ""))
        if run_id not in self.llm_runs:
            logger.debug(f"run_id {run_id} not found in llm_runs")
            return

        run_info = self.llm_runs.pop(run_id)
        duration = time.time() - run_info["start_time"]
        model_name = run_info["model"]

        # Debug logging
        logger.debug(f"on_llm_end called for run {run_id}")
        logger.debug(f"response.llm_output: {response.llm_output}")
        logger.debug(f"response.generations: {response.generations}")
        logger.debug(f"model_name = {model_name}")
        logger.debug(f"response.llm_output = {response.llm_output}")
        logger.debug(f"response attributes = {dir(response)}")

        # Check if response has usage_metadata attribute (newer LangChain versions)
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            logger.debug(f"response.usage_metadata = {response.usage_metadata}")
            usage_metadata = response.usage_metadata
            input_tokens = usage_metadata.get("input_tokens", 0)
            output_tokens = usage_metadata.get("output_tokens", 0)
            total_tokens = usage_metadata.get(
                "total_tokens", input_tokens + output_tokens
            )
        else:
            # Extract token usage from multiple possible locations
            token_usage = {}
            if response.llm_output:
                token_usage = response.llm_output.get("token_usage", {})
                if not token_usage and "usage" in response.llm_output:
                    token_usage = response.llm_output.get("usage", {})

            input_tokens = token_usage.get("prompt_tokens", 0)
            output_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", input_tokens + output_tokens)

            # Fallback: check generations for usage_metadata (newer OpenAI models)
            if total_tokens == 0 and response.generations:
                for generation_list in response.generations:
                    for generation in generation_list:
                        if hasattr(generation, "message") and hasattr(
                            generation.message, "usage_metadata"
                        ):
                            usage_metadata = generation.message.usage_metadata
                            if usage_metadata:
                                input_tokens = usage_metadata.get("input_tokens", 0)
                                output_tokens = usage_metadata.get("output_tokens", 0)
                                total_tokens = usage_metadata.get(
                                    "total_tokens", input_tokens + output_tokens
                                )
                                break

                        # Check generation_info for usage data
                        if (
                            hasattr(generation, "generation_info")
                            and generation.generation_info
                        ):
                            generation_info = generation.generation_info
                            logger.debug(f"generation_info = {generation_info}")

                            # Check for usage_metadata in generation_info
                            if "usage_metadata" in generation_info:
                                usage_metadata = generation_info["usage_metadata"]
                                input_tokens = usage_metadata.get("input_tokens", 0)
                                output_tokens = usage_metadata.get("output_tokens", 0)
                                total_tokens = usage_metadata.get(
                                    "total_tokens", input_tokens + output_tokens
                                )
                                break

                            # Check for direct usage fields
                            if "prompt_tokens" in generation_info:
                                input_tokens = generation_info.get("prompt_tokens", 0)
                                output_tokens = generation_info.get(
                                    "completion_tokens", 0
                                )
                                total_tokens = generation_info.get(
                                    "total_tokens", input_tokens + output_tokens
                                )
                                break

                    if total_tokens > 0:
                        break

        logger.debug(
            f"Extracted tokens - input: {input_tokens}, output: {output_tokens}, total: {total_tokens}"
        )

        # Track cost using CostTracker
        total_cost = self.cost_tracker.track_cost(
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        # Update tracer metrics if tracer is available
        if (
            hasattr(self, "tracer")
            and self.tracer
            and hasattr(self.tracer, "_ready")
            and self.tracer._ready
        ):
            try:
                timestamp = int(time.time() * 1000)

                # Use the specific run from our tracer instead of relying on active_run context
                if self.tracer._run and self.tracer._mlflow:
                    # Set our run as active temporarily for logging
                    with self.tracer._mlflow.start_run(
                        run_id=self.tracer._run.info.run_id
                    ):
                        logger.debug(
                            f"Using our specific run: {self.tracer._run.info.run_name} (ID: {self.tracer._run.info.run_id})"
                        )
                        # Use consistent metric names with CostTracker from monitor.py
                        self.tracer._mlflow.log_metric(
                            "llm_call_count", 1, step=timestamp
                        )
                        self.tracer._mlflow.log_metric(
                            "total_input_tokens", input_tokens, step=timestamp
                        )
                        self.tracer._mlflow.log_metric(
                            "total_output_tokens", output_tokens, step=timestamp
                        )
                        self.tracer._mlflow.log_metric(
                            "total_tokens", total_tokens, step=timestamp
                        )
                        self.tracer._mlflow.log_metric(
                            "duration_seconds", duration, step=timestamp
                        )
                        if total_cost > 0:
                            self.tracer._mlflow.log_metric(
                                "total_cost", total_cost, step=timestamp
                            )

                        logger.debug(
                            f"Logged LLM metrics: model={model_name}, tokens={total_tokens}, cost=${total_cost:.6f}"
                        )
            except Exception as e:
                logger.error(f"Failed to log LLM metrics: {e}")
        else:
            logger.debug("Tracer not ready, skipping metric logging")

        logger.debug(
            f"LLM run completed: model={model_name}, "
            f"tokens={total_tokens}, cost=${total_cost:.6f}"
        )

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs
    ) -> None:
        """Handle LLM errors."""
        run_id = str(kwargs.get("run_id", ""))
        if run_id in self.llm_runs:
            logger.warning(f"LLM run {run_id} failed: {error}")
            self.llm_runs.pop(run_id)


class MLflowLangflowTracer:
    """MLflow tracer for Langflow integration with native tracing support."""

    def __init__(
        self,
        trace_name: str,
        trace_type: str,
        project_name: str,
        trace_id: UUID,
        credential=None,
    ):
        self.trace_name = trace_name
        self.trace_type = trace_type
        self.project_name = project_name
        self.trace_id = trace_id
        self.flow_id = str(trace_id)

        # Debug logging for initialization
        logger.debug(
            f"MLflow Tracer initialized with trace_name='{trace_name}', trace_type='{trace_type}', flow_id='{self.flow_id[:8]}'"
        )

        self._ready = False
        self._run = None
        self._root_span_context = None
        self._spans: Dict[str, Dict[str, Any]] = {}  # Store span info
        self._callback_handler = None
        self._use_tracing = MLFLOW_TRACING_AVAILABLE
        self._mlflow_client = None
        self._mlflow = None  # Will hold either mlflow module or client.mlflow

        # Initialize MLflow
        self._setup_mlflow(credential)

    def _setup_mlflow(self, credential):
        """Setup MLflow client and experiment."""
        try:
            # Check if direct MLflow URI is set
            mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")

            if mlflow_uri:
                # Use mlflow directly since tracking URI is already set
                mlflow.set_tracking_uri(mlflow_uri)
                logger.debug(f"Using MLflow directly with tracking URI: {mlflow_uri}")
                self._mlflow_client = None
            else:
                # Use MLflowClient with credential
                if not credential:
                    # Create a ModelhubCredential instance using environment variables
                    try:
                        from autonomize.core.credential import ModelhubCredential

                        credential = ModelhubCredential(
                            modelhub_url=os.getenv("MODELHUB_URI")
                            or os.getenv("MODELHUB_BASE_URL"),
                            client_id=os.getenv("MODELHUB_AUTH_CLIENT_ID")
                            or os.getenv("MODELHUB_CLIENT_ID"),
                            client_secret=os.getenv("MODELHUB_AUTH_CLIENT_SECRET")
                            or os.getenv("MODELHUB_CLIENT_SECRET"),
                        )
                        logger.debug(
                            "Created ModelhubCredential from environment variables"
                        )
                    except Exception as e:
                        logger.warning(f"Failed to create ModelhubCredential: {e}")
                        return

                # Initialize MLflowClient with credential
                self._mlflow_client = MLflowClient(credential=credential)
                logger.debug("Using MLflow through MLflowClient with credential")

            # Set experiment
            experiment_name = (
                os.getenv("AUTONOMIZE_EXPERIMENT_NAME")
                or os.getenv("MLFLOW_EXPERIMENT_NAME")
                or os.getenv("EXPERIMENT_NAME")
                or self.project_name
                or "GenesisStudio"
            )

            if self._mlflow_client:
                self._mlflow_client.set_experiment(experiment_name=experiment_name)
                # Use mlflow from the client
                self._mlflow = self._mlflow_client.mlflow
            else:
                mlflow.set_experiment(experiment_name)
                self._mlflow = mlflow

            # Disable MLflow autolog to prevent duplicate runs - try multiple approaches
            try:
                logger.debug("MLflow Tracer: Attempting to disable autolog...")

                # Try disabling through our mlflow instance
                if hasattr(self._mlflow, "openai") and hasattr(
                    self._mlflow.openai, "autolog"
                ):
                    self._mlflow.openai.autolog(disable=True)
                    logger.debug("Disabled OpenAI autolog via self._mlflow")

                if hasattr(self._mlflow, "anthropic") and hasattr(
                    self._mlflow.anthropic, "autolog"
                ):
                    self._mlflow.anthropic.autolog(disable=True)
                    logger.debug("Disabled Anthropic autolog via self._mlflow")

                # Also try disabling through global mlflow module
                try:
                    import mlflow as global_mlflow

                    if hasattr(global_mlflow, "openai") and hasattr(
                        global_mlflow.openai, "autolog"
                    ):
                        global_mlflow.openai.autolog(disable=True)
                        logger.debug("Disabled OpenAI autolog via global mlflow")

                    if hasattr(global_mlflow, "anthropic") and hasattr(
                        global_mlflow.anthropic, "autolog"
                    ):
                        global_mlflow.anthropic.autolog(disable=True)
                        logger.debug("Disabled Anthropic autolog via global mlflow")
                except Exception as e:
                    logger.debug(f"MLflow Tracer: Error disabling global autolog: {e}")

                logger.debug("Disabled MLflow autolog to prevent duplicate runs")
            except Exception as e:
                logger.warning(f"Failed to disable autolog: {e}")
                logger.debug("MLflow Tracer: Error disabling autolog: {e}")

            # End any existing active run to ensure clean state
            try:
                active_run = self._mlflow.active_run()
                if active_run:
                    logger.debug(
                        f"MLflow Tracer: Found existing active run: {active_run.info.run_name}"
                    )
                    logger.debug(
                        f"Ending existing active run: {active_run.info.run_name}"
                    )
                    self._mlflow.end_run()
                    logger.debug("MLflow Tracer: Ended existing run")
                else:
                    logger.debug("MLflow Tracer: No existing active run found")
            except Exception as e:
                logger.warning(f"Failed to end existing run: {e}")
                logger.debug("MLflow Tracer: Error ending existing run: {e}")

            # Generate a better run name if we get generic names
            # Handle both "Untitled document" and "Untitled document - flow_id" patterns
            logger.debug(f"MLflow Tracer: Checking trace_name: '{self.trace_name}'")

            is_generic_name = (
                not self.trace_name
                or not self.trace_name.strip()
                or self.trace_name.lower() in ["untitled document", "untitled"]
                or self.trace_name.lower().startswith("untitled document -")
                or
                # Handle "Untitled document (24) - flow_id" pattern
                (
                    self.trace_name.lower().startswith("untitled document (")
                    and " - " in self.trace_name
                )
            )

            logger.debug(f"MLflow Tracer: is_generic_name = {is_generic_name}")

            if is_generic_name:
                # Generate a descriptive name based on timestamp for generic names
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                run_name = f"FlowExecuter_{timestamp}_{self.flow_id[:8]}"
                logger.debug(f"MLflow Tracer: Generated FlowExecuter name: {run_name}")
            else:
                # Use the provided trace name with flow ID
                clean_name = self.trace_name.replace(" ", "_").replace("-", "_")
                run_name = f"{clean_name}_{self.flow_id[:8]}"
                logger.debug(f"MLflow Tracer: Using trace name: {run_name}")

            # Check if there's still an active run before creating ours
            pre_run_check = self._mlflow.active_run()
            if pre_run_check:
                logger.debug(
                    f"MLflow Tracer: WARNING - Still have active run before creating: {pre_run_check.info.run_name}"
                )

            self._run = self._mlflow.start_run(
                run_name=run_name,
                tags={
                    "trace_id": str(self.trace_id),
                    "trace_type": self.trace_type,
                    "flow_id": self.flow_id,
                    "flow_name": self.trace_name,  # Store original trace_name as flow_name tag
                },
            )

            logger.debug(
                f"MLflow Tracer: Created run: {self._run.info.run_name} (ID: {self._run.info.run_id})"
            )

            # Verify this is the active run
            current_active = self._mlflow.active_run()
            if current_active:
                logger.debug(
                    f"MLflow Tracer: Current active run: {current_active.info.run_name} (ID: {current_active.info.run_id})"
                )
                if current_active.info.run_id != self._run.info.run_id:
                    logger.debug(
                        f"MLflow Tracer: WARNING - Active run mismatch! Our run: {self._run.info.run_id}, Active: {current_active.info.run_id}"
                    )
            else:
                logger.debug(f"MLflow Tracer: WARNING - No active run after creation!")

            # Log initial parameters
            self._mlflow.log_param("flow_name", self.trace_name)
            self._mlflow.log_param("trace_id", str(self.trace_id))

            # Check if MLflow 3.1.0+ tracing is available
            if self._use_tracing:
                try:
                    # MLflow 3.1.0+ uses start_span context manager
                    if hasattr(self._mlflow, "start_span"):
                        logger.info(
                            "MLflow 3.1.0+ tracing API detected - spans will be created"
                        )
                        # We'll create spans on-demand in add_trace/end_trace
                    else:
                        logger.info(
                            "MLflow start_span not available, using basic run tracking"
                        )
                        self._use_tracing = False
                except Exception as e:
                    logger.warning(f"MLflow tracing check failed: {e}")
                    self._use_tracing = False
            else:
                logger.info("MLflow tracing disabled")

            # Initialize callback handler
            self._callback_handler = MLflowLangChainCallback(self)

            self._ready = True
            logger.info(f"MLflow tracer initialized for flow: {self.flow_id}")

        except Exception as e:
            logger.error(f"Failed to setup MLflow: {e}")
            self._ready = False

    @property
    def ready(self) -> bool:
        """Check if tracer is ready."""
        return self._ready

    def add_trace(
        self,
        trace_id: str,
        trace_name: str,
        trace_type: str,
        inputs: dict[str, Any],
        metadata: dict[str, Any] | None = None,
        vertex: Any | None = None,
    ) -> None:
        """Add a new span to the trace."""
        if not self._ready:
            return

        # LOCAL OPERATIONS (immediate, non-blocking)
        start_time = time.time()

        # Store span info for later use (local operation)
        self._spans[trace_id] = {
            "name": trace_name,
            "type": trace_type,
            "inputs": inputs,
            "metadata": metadata,
            "start_time": start_time,
            "outputs": None,
            "error": None,
        }

        logger.debug(f"Started trace: {trace_name} ({trace_id})")

        # NETWORK OPERATIONS (async, non-blocking)
        # These will be queued and executed asynchronously
        try:
            # Queue network operations to prevent blocking
            self._queue_network_operation(
                self._log_component_start,
                (trace_id, trace_name, trace_type, start_time),
            )
        except Exception as e:
            logger.warning(f"Failed to queue trace start: {e}")

    def end_trace(
        self,
        trace_id: str,
        trace_name: str,
        outputs: dict[str, Any] | None = None,
        error: Exception | None = None,
        logs: Sequence[Any] = (),
    ) -> None:
        """End a span in the trace."""
        if not self._ready:
            return

        # LOCAL OPERATIONS (immediate, non-blocking)
        end_time = time.time()

        # Update span info if available (local operation)
        if trace_id in self._spans:
            span_info = self._spans[trace_id]
            span_info["outputs"] = outputs
            span_info["error"] = error
            span_info["end_time"] = end_time
            span_info["duration"] = end_time - span_info["start_time"]

        logger.debug(f"Ended trace: {trace_name} ({trace_id})")

        # NETWORK OPERATIONS (async, non-blocking)
        # These will be queued and executed asynchronously
        try:
            # Queue network operations to prevent blocking
            self._queue_network_operation(
                self._log_component_end, (trace_id, trace_name, end_time, error)
            )
        except Exception as e:
            logger.warning(f"Failed to queue trace end: {e}")

    def _queue_network_operation(self, func, args):
        """Queue a network operation for async execution."""
        # This will be overridden by the service to use its network queue
        # For now, execute immediately (fallback)
        try:
            func(*args)
        except Exception as e:
            logger.warning(f"Network operation failed: {e}")

    def _log_component_start(
        self, trace_id: str, trace_name: str, trace_type: str, start_time: float
    ):
        """Log component start metrics (network operation)."""
        try:
            self._mlflow.log_metric(f"component_{trace_id}_start", start_time)
            self._mlflow.log_param(f"component_{trace_id}_name", trace_name)
            self._mlflow.log_param(f"component_{trace_id}_type", trace_type)
        except Exception as e:
            logger.warning(f"Failed to log component start: {e}")

    def _log_component_end(
        self, trace_id: str, trace_name: str, end_time: float, error: Exception | None
    ):
        """Log component end metrics (network operation)."""
        try:
            self._mlflow.log_metric(f"component_{trace_id}_end", end_time)
            if error:
                self._mlflow.log_param(f"component_{trace_id}_error", str(error))
        except Exception as e:
            logger.warning(f"Failed to log component end: {e}")

    def set_network_queue(self, queue_func):
        """Set the network queue function from the tracing service."""
        self._queue_network_operation = queue_func

    def end(
        self,
        inputs: dict[str, Any],
        outputs: dict[str, Any],
        error: Exception | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """End the entire flow trace."""
        if not self._ready or not self._mlflow:
            return

        try:
            # Create spans using MLflow 3.1.0 API if available
            if self._use_tracing and hasattr(self._mlflow, "start_span"):
                # Use a clean trace name for the root span
                clean_trace_name = "FlowExecuter"
                if not (
                    not self.trace_name
                    or not self.trace_name.strip()
                    or self.trace_name.lower() in ["untitled document", "untitled"]
                    or self.trace_name.lower().startswith("untitled document -")
                    or (
                        self.trace_name.lower().startswith("untitled document (")
                        and " - " in self.trace_name
                    )
                ):
                    # Use the actual trace name if it's meaningful
                    clean_trace_name = self.trace_name.split(" - ")[
                        0
                    ]  # Remove flow ID suffix

                logger.debug(
                    f"MLflow Tracer: Creating root span with name: {clean_trace_name}"
                )

                # Create a single root span with all component information
                with self._mlflow.start_span(name=clean_trace_name) as root_span:
                    # Set inputs and outputs on root span
                    root_span.set_inputs(self._serialize_inputs(inputs))
                    root_span.set_outputs(self._serialize_inputs(outputs))

                    # Add attributes
                    root_span.set_attributes(
                        {
                            "trace_id": str(self.trace_id),
                            "flow_id": self.flow_id,
                            "trace_type": self.trace_type,
                            **(metadata or {}),
                        }
                    )

                    # Create child spans for each component
                    for trace_id, span_info in self._spans.items():
                        with self._mlflow.start_span(
                            name=span_info["name"]
                        ) as child_span:
                            # Set inputs/outputs
                            if span_info.get("inputs"):
                                child_span.set_inputs(
                                    self._serialize_inputs(span_info["inputs"])
                                )
                            if span_info.get("outputs"):
                                child_span.set_outputs(
                                    self._serialize_inputs(span_info["outputs"])
                                )

                            # Set attributes
                            child_span.set_attributes(
                                {
                                    "component_id": trace_id,
                                    "component_type": span_info["type"],
                                    **(span_info.get("metadata") or {}),
                                }
                            )

                            # Set status based on error
                            if span_info.get("error"):
                                child_span.set_status("ERROR")
                                child_span.set_attribute(
                                    "error", str(span_info["error"])
                                )
                            else:
                                child_span.set_status("OK")

            # Log artifacts
            self._mlflow.log_dict(self._serialize_inputs(inputs), "flow_inputs.json")
            self._mlflow.log_dict(self._serialize_inputs(outputs), "flow_outputs.json")

            if metadata:
                self._mlflow.log_dict(metadata, "flow_metadata.json")

            # Log cost metrics
            if hasattr(self, "cost_metrics"):
                self._mlflow.log_metrics(
                    {
                        "total_tokens": self.cost_metrics.get("total_tokens", 0),
                        "input_tokens": self.cost_metrics.get("input_tokens", 0),
                        "output_tokens": self.cost_metrics.get("output_tokens", 0),
                        "total_cost": self.cost_metrics.get("total_cost", 0.0),
                    }
                )

            # End MLflow run
            self._mlflow.end_run(status="FAILED" if error else "FINISHED")

            logger.info(f"Ended MLflow trace for flow: {self.flow_id}")

        except Exception as e:
            logger.warning(f"Failed to end flow: {e}")

    def update_cost_metrics(self, token_usage: dict[str, Any], cost: float) -> None:
        """Update cost metrics."""
        if not hasattr(self, "cost_metrics"):
            self.cost_metrics = {
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
            }

        self.cost_metrics["input_tokens"] += token_usage.get("input_tokens", 0)
        self.cost_metrics["output_tokens"] += token_usage.get("output_tokens", 0)
        self.cost_metrics["total_tokens"] += token_usage.get("total_tokens", 0)
        self.cost_metrics["total_cost"] += cost

    def get_langchain_callback(self) -> BaseCallbackHandler | None:
        """Get LangChain callback handler."""
        return self._callback_handler

    def _serialize_inputs(self, data: Any) -> Any:
        """Ensure data is JSON serializable."""
        try:
            json.dumps(data)
            return data
        except (TypeError, ValueError):
            # Convert non-serializable objects
            return json.loads(json.dumps(data, default=str))


def get_mlflow_client():
    """Get MLflow client instance."""
    return mlflow


def get_mlflow_langchain_callback(tracer):
    """Get MLflow LangChain callback."""
    if hasattr(tracer, "_callback_handler"):
        return tracer._callback_handler
    return MLflowLangChainCallback(tracer)
