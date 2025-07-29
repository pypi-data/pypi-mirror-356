# ml_observability/observability/langflow_async_tracer.py
import asyncio
import uuid
import time
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Union
from collections import defaultdict

try:
    import mlflow
    from mlflow.tracking import MlflowClient
except ImportError:
    mlflow = None
    MlflowClient = None

from ..utils.logger import setup_logger
from .base_tracer import BaseTracer
from .cost_tracking import CostTracker

# LangChain imports
try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import LLMResult
    from langchain_core.outputs import Generation, ChatGeneration
except ImportError:
    # Create dummy classes if LangChain is not available
    BaseCallbackHandler = object
    LLMResult = object
    Generation = object
    ChatGeneration = object

logger = setup_logger(__name__)


class MLflowLangChainCallbackHandler(BaseCallbackHandler):
    """
    Custom MLflow callback handler for LangChain that captures token usage and cost.
    """

    def __init__(self, tracer_instance):
        super().__init__()
        self.tracer = tracer_instance
        self.llm_runs: Dict[str, Dict] = {}
        self.cost_tracker = CostTracker()

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs
    ) -> None:
        run_id = str(kwargs.get("run_id"))
        if not run_id:
            return

        model_name = "unknown"
        if "id" in serialized and isinstance(serialized["id"], list):
            model_name = serialized["id"][-1]

        self.llm_runs[run_id] = {
            "start_time": time.time(),
            "prompts": prompts,
            "model_name": model_name,
        }
        logger.debug(
            f"🎯 LLM_CALLBACK: Started LLM run {run_id} with model {model_name}"
        )

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        run_id = str(kwargs.get("run_id"))
        if run_id not in self.llm_runs:
            return

        run_info = self.llm_runs.pop(run_id)
        duration = time.time() - run_info["start_time"]
        model_name = run_info["model_name"]

        token_usage = {}
        if response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})
            if not token_usage and "usage" in response.llm_output:  # Azure
                token_usage = response.llm_output.get("usage", {})

        input_tokens = token_usage.get("prompt_tokens", 0)
        output_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get("total_tokens", 0)

        if total_tokens == 0:
            total_tokens = input_tokens + output_tokens

        # Fallback for models that do not return token usage in llm_output
        # but include it in generation_info
        if total_tokens == 0:
            for gen_list in response.generations:
                for gen in gen_list:
                    if gen.generation_info:
                        usage_metadata = gen.generation_info.get("usage_metadata")
                        if usage_metadata:
                            input_tokens += usage_metadata.get("input_tokens", 0)
                            output_tokens += usage_metadata.get("output_tokens", 0)
            total_tokens = input_tokens + output_tokens

        total_cost = self.cost_tracker.track_cost(
            model_name, input_tokens, output_tokens
        )

        logger.debug(f"💰 LLM_CALLBACK: Captured token usage for {model_name}: "
                    f"in={input_tokens}, out={output_tokens}, cost=${total_cost:.6f}")

        cost_info = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "model_name": model_name,
            "duration_seconds": duration,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.tracer._add_llm_cost_info(cost_info)

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs
    ) -> None:
        run_id = str(kwargs.get("run_id"))
        if run_id in self.llm_runs:
            logger.warning(f"🚨 LLM_CALLBACK: LLM run {run_id} failed: {error}")
            self.llm_runs.pop(run_id)


class LangflowAsyncTracer(BaseTracer):
    """Async tracer for LangFlow with MLflow integration and automatic token tracking."""

    def __init__(
        self, trace_name: str, trace_type: str, project_name: str, trace_id: uuid.UUID
    ):
        super().__init__(trace_name, trace_type, project_name, trace_id)
        self._is_initialized = False
        self._mlflow_client = None
        self._experiment_id = None
        self._flow_runs = {}
        self._flow_data = defaultdict(dict)
        self._flow_orders = defaultdict(list)
        self._flow_traces = {}
        self._llm_cost_info = []

        self._callback_handler = (
            MLflowLangChainCallbackHandler(self)
            if BaseCallbackHandler != object
            else None
        )

        if self._has_event_loop():
            asyncio.create_task(self._async_init())
        else:
            self._sync_init()

    def _has_event_loop(self) -> bool:
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False

    def _sync_init(self):
        if self._is_initialized:
            return
        if mlflow:
            self._mlflow_client = MlflowClient()
            self._experiment_id = self._get_or_create_experiment(self.project_name)
            self._is_initialized = True
            logger.debug("✅ MLflow tracer initialized synchronously.")
        else:
            logger.warning("⚠️ MLflow is not installed. Tracing is disabled.")

    async def _async_init(self):
        if self._is_initialized:
            return
        await asyncio.to_thread(self._sync_init)

    @property
    def ready(self) -> bool:
        return self._is_initialized

    def _get_flow_key(self, trace_id: str = None) -> str:
        return str(self.trace_id)

    def _get_or_create_experiment(self, name: str) -> Optional[str]:
        if not self._mlflow_client:
            return None
        experiment = self._mlflow_client.get_experiment_by_name(name)
        if experiment:
            return experiment.experiment_id
        return self._mlflow_client.create_experiment(name)

    def add_trace(
        self,
        trace_id: str,
        trace_name: str,
        trace_type: str,
        inputs: dict[str, Any],
        metadata: dict[str, Any] | None = None,
        vertex: Any | None = None,
    ) -> None:
        if not self.ready:
            self._sync_init()

        flow_key = self._get_flow_key()
        if flow_key not in self._flow_runs:
            self._start_flow_run_and_trace(flow_key)

        self._flow_orders[flow_key].append(trace_id)
        self._flow_data[flow_key][trace_id] = {
            "trace_id": trace_id,
            "trace_name": trace_name,
            "trace_type": trace_type,
            "inputs": inputs,
            "metadata": metadata or {},
            "vertex": vertex,
            "start_time": time.time(),
            "outputs": None,
            "error": None,
            "success": False,
            "duration_seconds": 0,
        }
        logger.debug(
            f"📊 Added component trace: {trace_name} ({trace_id}) to agent run {flow_key}"
        )

    def _start_flow_run_and_trace(self, flow_key: str):
        if not self._mlflow_client:
            return

        run = self._mlflow_client.create_run(
            experiment_id=self._experiment_id,
            tags={"mlflow.runName": f"Agent Run - {self.trace_name} - {flow_key}"},
        )
        self._flow_runs[flow_key] = run
        logger.info(
            f"🚀 Started new MLflow run: {run.info.run_id} for agent run {flow_key}"
        )

    def end_trace(
        self,
        trace_id: str,
        trace_name: str,
        outputs: dict[str, Any] | None = None,
        error: Exception | None = None,
        logs: Sequence[Any] = (),
    ) -> None:
        flow_key = self._get_flow_key()
        if trace_id not in self._flow_data[flow_key]:
            return

        component_data = self._flow_data[flow_key][trace_id]
        end_time = time.time()
        duration = end_time - component_data["start_time"]

        component_data.update(
            {
                "outputs": outputs,
                "error": str(error) if error else None,
                "success": error is None,
                "duration_seconds": duration,
            }
        )
        logger.debug(f"✅ Ended component trace: {trace_name} ({trace_id})")

    def end(
        self,
        inputs: dict[str, Any],
        outputs: dict[str, Any],
        error: Exception | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        flow_key = self._get_flow_key()
        if flow_key not in self._flow_runs:
            logger.warning(
                f"⚠️ Attempted to end an agent run that was not started: {flow_key}"
            )
            return

        run_id = self._flow_runs[flow_key].info.run_id

        try:
            with mlflow.start_run(run_id=run_id, nested=False):
                # Log metrics and artifacts first
                mlflow.log_dict(self._serialize_io(inputs), "flow_inputs.json")
                mlflow.log_dict(self._serialize_io(outputs), "flow_outputs.json")

                if self._llm_cost_info:
                    total_cost = sum(c["total_cost"] for c in self._llm_cost_info)
                    total_input_tokens = sum(
                        c["input_tokens"] for c in self._llm_cost_info
                    )
                    total_output_tokens = sum(
                        c["output_tokens"] for c in self._llm_cost_info
                    )
                    total_tokens = sum(c["total_tokens"] for c in self._llm_cost_info)

                    mlflow.log_metric("total_cost", round(total_cost, 6))
                    mlflow.log_metric("total_input_tokens", total_input_tokens)
                    mlflow.log_metric("total_output_tokens", total_output_tokens)
                    mlflow.log_metric("total_tokens", total_tokens)

                    mlflow.log_dict(self._llm_cost_info, "llm_costs_details.json")

                # Log overall agent run metrics
                flow_data = self._flow_data.get(flow_key, {})
                component_count = len(flow_data)
                success_components = sum(
                    1 for c in flow_data.values() if c.get("success")
                )

                mlflow.log_metric(
                    "total_agent_duration_seconds",
                    round(time.time() - self.start_time, 4),
                )
                mlflow.log_metric("component_count", component_count)
                mlflow.log_metric("success_components", success_components)
                mlflow.log_metric(
                    "error_components", component_count - success_components
                )

                # Now, create the trace using a root span and nested child spans
                with mlflow.start_span(name=self.trace_name) as root_span:
                    root_span.set_inputs(self._serialize_io(inputs))
                    if outputs:
                        root_span.set_outputs(self._serialize_io(outputs))
                    if error:
                        root_span.set_attribute("error", str(error))

                    # Reconstruct component spans
                    flow_order = self._flow_orders.get(flow_key, [])

                    for trace_id in flow_order:
                        component_data = flow_data.get(trace_id)
                        if not component_data:
                            continue

                        span_name = f"{component_data['trace_name']}"

                        with mlflow.start_span(name=span_name) as child_span:
                            child_span.set_inputs(
                                self._serialize_io(component_data.get("inputs", {}))
                            )

                            if component_data.get("outputs"):
                                child_span.set_outputs(
                                    self._serialize_io(component_data.get("outputs"))
                                )

                            attributes = {
                                "vertex_id": component_data["trace_id"],
                                "vertex_type": component_data["trace_type"],
                                "duration_seconds": round(
                                    component_data.get("duration_seconds", 0), 4
                                ),
                                "success": component_data.get("success", False),
                            }
                            if component_data.get("error"):
                                attributes["error"] = component_data["error"]

                            # Add component metadata as attributes
                            if component_data.get("metadata"):
                                for key, value in component_data["metadata"].items():
                                    try:
                                        attributes[key] = str(value)
                                    except:
                                        pass  # Ignore metadata that can't be stringified

                            child_span.set_attributes(attributes)

            logger.info(
                f"✅ Successfully ended MLflow run {run_id} and trace for agent {self.trace_name}"
            )
        except Exception as e:
            logger.error(
                f"❌ Failed to end MLflow run and trace for agent {self.trace_name}: {e}",
                exc_info=True,
            )
        finally:
            self._cleanup_flow(flow_key)

    def _cleanup_flow(self, flow_key: str):
        self._flow_runs.pop(flow_key, None)
        self._flow_data.pop(flow_key, None)
        self._flow_orders.pop(flow_key, None)
        self._flow_traces.pop(flow_key, None)
        self._llm_cost_info.clear()
        logger.debug(f"🧹 Cleaned up resources for agent run {flow_key}")

    def _add_llm_cost_info(self, cost_info: Dict[str, Any]):
        self._llm_cost_info.append(cost_info)

    def get_langchain_callback(self):
        """
        Returns an instance of the LangChain callback handler.
        If LangChain is not installed, returns None.
        """
        return self._callback_handler

    def _serialize_io(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures that the input/output data is JSON serializable."""
        if not data:
            return {}
        try:
            # Attempt to serialize to catch errors early
            json.dumps(data)
            return data
        except (TypeError, OverflowError):
            return json.loads(json.dumps(data, default=str))
