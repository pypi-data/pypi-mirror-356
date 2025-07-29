# ml_observability/observability/langflow_async_tracer.py
import asyncio
import uuid
import time
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Union
from collections import defaultdict

try:
    import mlflow
    from mlflow.tracking import MlflowClient
except ImportError:
    mlflow = None
    MlflowClient = None

from autonomize.core.credential import ModelhubCredential
from ..utils.logger import setup_logger
from .base_tracer import BaseTracer
from .cost_tracking import CostTracker
from ml_observability.core.mlflow_client import MLflowClient as CustomMLflowClient

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

# Global instances - following monitor.py pattern
_mlflow_client: Optional[CustomMLflowClient] = None
_cost_tracker: Optional[CostTracker] = None
_initialized: bool = False


def initialize_tracer(
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[ModelhubCredential] = None,
):
    """
    Initialize the MLflowClient and CostTracker for the tracer.
    Must be called once at startup - follows monitor.py pattern.

    Args:
        cost_rates (dict, optional): Dictionary of cost rates for different models
        experiment_name (str, optional): Name of the MLflow experiment
        credential (ModelhubCredential, optional): Modelhub credentials
    """
    global _mlflow_client, _cost_tracker, _initialized

    # Check if already initialized
    if _initialized:
        logger.debug("Langflow tracer already initialized, skipping.")
        return

    # Check if MLFLOW_TRACKING_URI is set in environment
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

    if mlflow_tracking_uri:
        # Use mlflow directly since tracking URI is already set
        logger.debug("Using MLflow directly with tracking URI: %s", mlflow_tracking_uri)
        _mlflow_client = None
    else:
        if not credential:
            # Create a ModelhubCredential instance using environment variables.
            credential = ModelhubCredential()

        _mlflow_client = CustomMLflowClient(credential=credential)

    experiment_name = experiment_name or os.getenv("EXPERIMENT_NAME")
    if experiment_name:
        if _mlflow_client:
            _mlflow_client.set_experiment(experiment_name=experiment_name)
        else:
            mlflow.set_experiment(experiment_name)

    _cost_tracker = CostTracker(cost_rates=cost_rates)

    # Mark as initialized
    _initialized = True
    logger.debug("Langflow tracer initialized.")


class MLflowLangChainCallbackHandler(BaseCallbackHandler):
    """
    Custom MLflow callback handler for LangChain that captures token usage and cost.
    """

    def __init__(self, tracer_instance):
        super().__init__()
        self.tracer = tracer_instance
        self.llm_runs: Dict[str, Dict] = {}

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
        global _cost_tracker
        
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

        total_cost = 0
        if _cost_tracker:
            total_cost = _cost_tracker.track_cost(model_name, input_tokens, output_tokens)

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
        
        # Initialize the global tracer system if not already done
        initialize_tracer()
        
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

        # Set up experiment
        if self.ready:
            self._experiment_id = self._get_or_create_experiment(self.project_name)

    @property
    def ready(self) -> bool:
        return _initialized

    def _get_flow_key(self, trace_id: str = None) -> str:
        return str(self.trace_id)

    def _get_or_create_experiment(self, name: str) -> Optional[str]:
        global _mlflow_client
        
        if _mlflow_client:
            # Use the underlying mlflow client through the mlflow property
            experiment = _mlflow_client.mlflow.get_experiment_by_name(name)
            if experiment:
                return experiment.experiment_id
            return _mlflow_client.mlflow.create_experiment(name)
        elif mlflow:
            experiment = mlflow.get_experiment_by_name(name)
            if experiment:
                return experiment.experiment_id
            return mlflow.create_experiment(name)
        return None

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
            logger.warning("Tracer not ready, skipping trace")
            return

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
        global _mlflow_client
        
        if _mlflow_client:
            # Use the underlying mlflow client through the mlflow property
            run = _mlflow_client.mlflow.start_run(
                experiment_id=self._experiment_id,
                run_name=f"Agent Run - {self.trace_name} - {flow_key}",
            )
        elif mlflow:
            run = mlflow.start_run(
                experiment_id=self._experiment_id,
                run_name=f"Agent Run - {self.trace_name} - {flow_key}",
            )
        else:
            logger.warning("No MLflow client available")
            return
            
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

        trace_data = self._flow_data[flow_key][trace_id]
        trace_data["outputs"] = outputs
        trace_data["error"] = error
        trace_data["success"] = error is None
        trace_data["duration_seconds"] = time.time() - trace_data["start_time"]

        logger.debug(
            f"📋 Ended component trace: {trace_name} ({trace_id}) - "
            f"Success: {trace_data['success']}, Duration: {trace_data['duration_seconds']:.2f}s"
        )

    def end(
        self,
        inputs: dict[str, Any],
        outputs: dict[str, Any],
        error: Exception | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        flow_key = self._get_flow_key()
        if flow_key not in self._flow_runs:
            logger.warning(f"No active run found for flow {flow_key}")
            return

        try:
            self._log_final_metrics_and_trace(flow_key, inputs, outputs, error)
            logger.info(f"✅ Successfully logged final metrics for flow {flow_key}")
        except Exception as e:
            logger.error(f"❌ Error logging final metrics: {e}")
        finally:
            self._cleanup_flow(flow_key)

    def _log_final_metrics_and_trace(self, flow_key, inputs, outputs, error):
        global _mlflow_client
        
        run = self._flow_runs[flow_key]
        
        if _mlflow_client:
            # Use the underlying mlflow client through the mlflow property
            with _mlflow_client.mlflow.start_run(run_id=run.info.run_id):
                _mlflow_client.mlflow.log_dict(self._serialize_io(inputs), "flow_inputs.json")
                _mlflow_client.mlflow.log_dict(self._serialize_io(outputs), "flow_outputs.json")
                if error: 
                    _mlflow_client.mlflow.set_tag("status", "FAILED")
                
                flow_data = self._flow_data.get(flow_key, {})
                all_costs = [cost for data in flow_data.values() if "llm_costs" in data for cost in data["llm_costs"]]
                if all_costs:
                    _mlflow_client.mlflow.log_metric("total_cost", sum(c.get("total_cost", 0) for c in all_costs))
        elif mlflow:
            mlflow.log_dict(self._serialize_io(inputs), "flow_inputs.json")
            mlflow.log_dict(self._serialize_io(outputs), "flow_outputs.json")
            if error: 
                mlflow.set_tag("status", "FAILED")
            
            flow_data = self._flow_data.get(flow_key, {})
            all_costs = [cost for data in flow_data.values() if "llm_costs" in data for cost in data["llm_costs"]]
            if all_costs:
                mlflow.log_metric("total_cost", sum(c.get("total_cost", 0) for c in all_costs))

    def _cleanup_flow(self, flow_key: str):
        if flow_key in self._flow_runs:
            del self._flow_runs[flow_key]
        if flow_key in self._flow_data:
            del self._flow_data[flow_key]
        if flow_key in self._flow_orders:
            del self._flow_orders[flow_key]

    def _add_llm_cost_info(self, cost_info: Dict[str, Any]):
        self._llm_cost_info.append(cost_info)

    def get_langchain_callback(self):
        """Return a new callback handler instance for the current component context."""
        if not self.ready:
            logger.warning("Tracer not ready, returning None callback")
            return None
        return MLflowLangChainCallbackHandler(self)

    def _serialize_io(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize inputs/outputs for MLflow logging."""
        try:
            return json.loads(json.dumps(data, default=str))
        except Exception as e:
            logger.warning(f"Failed to serialize data: {e}")
            return {"error": "Failed to serialize data", "raw": str(data)}
