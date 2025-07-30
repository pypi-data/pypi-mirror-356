"""MLflow tracer for Langflow using MLflow's native tracing API with nested spans."""

from __future__ import annotations
import asyncio
import uuid
import time
import json
import threading
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Union
from collections import defaultdict
from contextlib import contextmanager

import mlflow
from mlflow.tracking import MlflowClient
# MLflow tracing imports
from mlflow.tracing import set_span_attribute, start_span
from mlflow.entities import SpanType, SpanStatus, SpanStatusCode


# Import custom MLflowClient if available
from ml_observability.core.mlflow_client import MLflowClient as CustomMLflowClient
from autonomize.core.credential import ModelhubCredential

from ..utils.logger import setup_logger
from .base_tracer import BaseTracer
from .cost_tracking import CostTracker

# LangChain imports
try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import LLMResult
    from langchain_core.outputs import Generation, ChatGeneration
except ImportError:
    BaseCallbackHandler = object
    LLMResult = object
    Generation = object
    ChatGeneration = object

logger = setup_logger(__name__)


class MLflowLangChainCallbackHandler(BaseCallbackHandler):
    """
    Custom MLflow callback handler for LangChain that captures token usage and cost.
    Uses MLflow's tracing API for thread-safe span management.
    """
    def __init__(self, tracer_instance):
        super().__init__()
        self.tracer = tracer_instance
        self.llm_runs: Dict[str, Dict] = {}
        self.cost_tracker = CostTracker()

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        run_id = str(kwargs.get("run_id", uuid.uuid4()))
        
        model_name = "unknown"
        if "id" in serialized and isinstance(serialized["id"], list):
            model_name = serialized["id"][-1]
        elif "name" in kwargs:
            model_name = kwargs["name"]
        
        # Normalize model names
        if model_name.lower() in ["chatopenai", "openai"]:
            model_name = kwargs.get("model", "gpt-3.5-turbo")

        self.llm_runs[run_id] = {
            "start_time": time.time(),
            "prompts": prompts,
            "model_name": model_name,
        }
        logger.debug(f"🎯 LLM_CALLBACK: Started LLM run {run_id} with model {model_name}")

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        run_id = str(kwargs.get("run_id"))
        if run_id not in self.llm_runs:
            return

        run_info = self.llm_runs.pop(run_id)
        duration = time.time() - run_info["start_time"]
        model_name = run_info["model_name"]
        
        # Extract token usage
        token_usage = {}
        if response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})
            if not token_usage and 'usage' in response.llm_output:
                token_usage = response.llm_output.get("usage", {})
            if 'model_name' in response.llm_output:
                model_name = response.llm_output['model_name']

        input_tokens = token_usage.get("prompt_tokens", 0)
        output_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get("total_tokens", input_tokens + output_tokens)

        # Track cost
        total_cost = self.cost_tracker.track_cost(
            model_name, input_tokens, output_tokens
        )
        
        # Set attributes on current span if available
        try:
            if set_span_attribute:
                set_span_attribute(f"llm.{model_name}.input_tokens", input_tokens)
                set_span_attribute(f"llm.{model_name}.output_tokens", output_tokens)
                set_span_attribute(f"llm.{model_name}.total_tokens", total_tokens)
                set_span_attribute(f"llm.{model_name}.cost", total_cost)
                set_span_attribute(f"llm.{model_name}.duration_s", duration)
        except Exception as e:
            logger.debug(f"Could not set span attributes: {e}")
        
        logger.info(f"💰 LLM_CALLBACK: Captured token usage for {model_name}: "
                    f"in={input_tokens}, out={output_tokens}, cost=${total_cost:.6f}")

        # Store cost info for summary
        cost_info = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "model_name": model_name,
            "duration_seconds": duration,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.tracer._add_llm_cost_info(cost_info)

    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs) -> None:
        run_id = str(kwargs.get("run_id"))
        if run_id in self.llm_runs:
            logger.warning(f"🚨 LLM_CALLBACK: LLM run {run_id} failed: {error}")
            self.llm_runs.pop(run_id)


class LangflowAsyncTracer(BaseTracer):
    """
    MLflow tracer for Langflow using MLflow's native tracing API.
    Creates a single run with nested spans for component hierarchy.
    """

    def __init__(
        self, trace_name: str, trace_type: str, project_name: str, trace_id: uuid.UUID
    ):
        super().__init__(trace_name, trace_type, project_name, trace_id)
        self._is_initialized = False
        self._mlflow_client = None
        self._custom_mlflow_client = None  # For custom MLflowClient
        self._experiment_id = None
        self._run_id = None
        self._root_span = None
        self._component_spans = {}  # trace_id -> span mapping
        self._flow_data = defaultdict(dict)
        self._flow_orders = defaultdict(list)
        self._llm_cost_info = []
        
        # Initialize synchronously
        self._sync_init()
        
        # Create callback handler
        self._callback_handler = (
            MLflowLangChainCallbackHandler(self) 
            if BaseCallbackHandler != object else None
        )
    
    def _sync_init(self):
        """Initialize MLflow client and experiment using the same pattern as monitor.py."""
        if self._is_initialized:
            return
            
        if not mlflow:
            logger.warning("⚠️ MLflow is not installed. Tracing is disabled.")
            return
            
        try:
            # Check if MLFLOW_TRACKING_URI is set in environment
            mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
            
            if mlflow_tracking_uri:
                # Use mlflow directly since tracking URI is already set
                logger.debug("Using MLflow directly with tracking URI: %s", mlflow_tracking_uri)
                self._mlflow_client = MlflowClient()
                self._custom_mlflow_client = None
            else:
                # Try to use custom MLflowClient if available
                if CustomMLflowClient and ModelhubCredential:
                    try:
                        credential = ModelhubCredential()
                        self._custom_mlflow_client = CustomMLflowClient(credential=credential)
                        self._mlflow_client = MlflowClient()
                        logger.debug("Using custom MLflowClient with ModelhubCredential")
                    except Exception as e:
                        logger.warning(f"Failed to initialize custom MLflowClient: {e}")
                        # Fallback to standard MLflow client
                        self._mlflow_client = MlflowClient()
                        self._custom_mlflow_client = None
                else:
                    # Use standard MLflow client
                    self._mlflow_client = MlflowClient()
                    self._custom_mlflow_client = None
            
            # Set experiment
            experiment_name = os.getenv("EXPERIMENT_NAME", self.project_name)
            if self._custom_mlflow_client:
                self._custom_mlflow_client.set_experiment(experiment_name=experiment_name)
                self._experiment_id = self._get_or_create_experiment(experiment_name)
            else:
                mlflow.set_experiment(experiment_name)
                self._experiment_id = self._get_or_create_experiment(experiment_name)
            
            # Check if there's already an active run
            active_run = mlflow.active_run()
            if active_run:
                # Use the existing active run
                self._run_id = active_run.info.run_id
                logger.info(f"📌 Using existing MLflow run: {self._run_id}")
            else:
                # Create a new run for this flow
                run = mlflow.start_run(
                    run_name=f"{self.trace_name} - {self.trace_id}",
                    experiment_id=self._experiment_id,
                    tags={
                        "flow_name": self.trace_name,
                        "trace_id": str(self.trace_id),
                        "trace_type": self.trace_type
                    }
                )
                self._run_id = run.info.run_id
                logger.info(f"✅ Created MLflow run: {self._run_id}")
            
            # Log initial parameters
            if self._custom_mlflow_client:
                self._custom_mlflow_client.log_param("flow_name", self.trace_name)
                self._custom_mlflow_client.log_param("trace_type", self.trace_type)
            else:
                mlflow.log_param("flow_name", self.trace_name)
                mlflow.log_param("trace_type", self.trace_type)
            
            self._is_initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize MLflow tracer: {e}")
            self._is_initialized = False

    @property
    def ready(self) -> bool:
        return self._is_initialized and self._mlflow_client is not None

    def _get_or_create_experiment(self, name: str) -> Optional[str]:
        """Get or create MLflow experiment."""
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
        """Start a new component trace as a nested span."""
        if not self.ready:
            return
        
        try:
            # Extract component name without ID
            component_name = trace_name.split(" (")[0] if " (" in trace_name else trace_name
            
            # Determine span type based on trace_type
            span_type = SpanType.CHAIN if SpanType else "CHAIN"
            if trace_type == "llm":
                span_type = SpanType.LLM if SpanType else "LLM"
            elif trace_type == "tool":
                span_type = SpanType.TOOL if SpanType else "TOOL"
            elif trace_type == "retriever":
                span_type = SpanType.RETRIEVER if SpanType else "RETRIEVER"
            
            # Start a new span for this component using the correct start_span function
            span = start_span(
                name=component_name,
                span_type=span_type,
                parent_id=getattr(self._root_span, 'span_id', None) if self._root_span else None,
                attributes={
                    "component_id": trace_id,
                    "component_type": trace_type,
                    "component_full_name": trace_name,
                }
            )
            
            # Set inputs on the span using a context manager pattern
            with span:
                if hasattr(span, 'set_inputs'):
                    span.set_inputs(self._serialize_io(inputs))
            
            # Store span reference
            self._component_spans[trace_id] = span
            
            # Store component data
            flow_key = self._get_flow_key()
            self._flow_orders[flow_key].append(trace_id)
            self._flow_data[flow_key][trace_id] = {
                "trace_id": trace_id,
                "trace_name": trace_name,
                "trace_type": trace_type,
                "inputs": inputs,
                "metadata": metadata or {},
                "vertex": vertex,
                "start_time": time.time(),
                "span": span,
                "outputs": None,
                "error": None,
                "success": False,
                "duration_seconds": 0,
            }
            
            logger.debug(f"📊 Started component span: {trace_name} ({trace_id})")
            
        except Exception as e:
            logger.error(f"Failed to start component trace: {e}")

    def end_trace(
        self,
        trace_id: str,
        trace_name: str,
        outputs: dict[str, Any] | None = None,
        error: Exception | None = None,
        logs: Sequence[Any] = (),
    ) -> None:
        """End a component trace span."""
        flow_key = self._get_flow_key()
        if trace_id not in self._flow_data[flow_key]:
            return

        component_data = self._flow_data[flow_key][trace_id]
        span = component_data.get("span")
        if not span:
            return
            
        end_time = time.time()
        duration = end_time - component_data["start_time"]

        component_data.update({
            "outputs": outputs,
            "error": str(error) if error else None,
            "success": error is None,
            "duration_seconds": duration,
        })
        
        try:
            # Set outputs and attributes on the span using context manager if available
            with span:
                if outputs and hasattr(span, 'set_outputs'):
                    span.set_outputs(self._serialize_io(outputs))
                
                # Set attributes
                if hasattr(span, 'set_attribute'):
                    span.set_attribute("duration_seconds", duration)
                    span.set_attribute("success", error is None)
                
                # Set error if present
                if error and hasattr(span, 'set_attribute'):
                    span.set_attribute("error", str(error))
                    # Use SpanStatus object or status code string
                    if hasattr(span, 'set_status'):
                        if SpanStatus and SpanStatusCode:  # MLflow tracing is available
                            span.set_status(SpanStatus(SpanStatusCode.ERROR))
                        else:
                            span.set_status("ERROR")
                else:
                    if hasattr(span, 'set_status'):
                        if SpanStatus and SpanStatusCode:  # MLflow tracing is available
                            span.set_status(SpanStatus(SpanStatusCode.OK))
                        else:
                            span.set_status("OK")
                
                # End the span
                if hasattr(span, 'end'):
                    span.end()
            
            logger.debug(f"✅ Ended component span: {trace_name} ({trace_id})")
            
        except Exception as e:
            logger.error(f"Failed to end component trace: {e}")

    def end(
        self,
        inputs: dict[str, Any],
        outputs: dict[str, Any],
        error: Exception | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """End the flow trace and log final metrics."""
        if not self.ready:
            return
        
        try:
            # Create root span for the entire flow if not exists
            if not self._root_span:
                self._root_span = start_span(
                    name=self.trace_name,
                    span_type=SpanType.CHAIN if SpanType else "CHAIN",
                )
                with self._root_span:
                    if hasattr(self._root_span, 'set_inputs'):
                        self._root_span.set_inputs(self._serialize_io(inputs))
            
            # Set outputs and status on root span using context manager
            with self._root_span:
                # Set outputs on root span
                if outputs and hasattr(self._root_span, 'set_outputs'):
                    self._root_span.set_outputs(self._serialize_io(outputs))
                
                # Set error if present
                if error and hasattr(self._root_span, 'set_attribute'):
                    self._root_span.set_attribute("error", str(error))
                    # Use SpanStatus object or status code string
                    if hasattr(self._root_span, 'set_status'):
                        if SpanStatus and SpanStatusCode:  # MLflow tracing is available
                            self._root_span.set_status(SpanStatus(SpanStatusCode.ERROR))
                        else:
                            self._root_span.set_status("ERROR")
                else:
                    if hasattr(self._root_span, 'set_status'):
                        if SpanStatus and SpanStatusCode:  # MLflow tracing is available
                            self._root_span.set_status(SpanStatus(SpanStatusCode.OK))
                        else:
                            self._root_span.set_status("OK")
                
                # End root span
                if hasattr(self._root_span, 'end'):
                    self._root_span.end()
            
            # Log artifacts and metrics to the run
            if self._custom_mlflow_client:
                # Use mlflow directly for logging since custom client doesn't have log_dict
                mlflow.log_dict(self._serialize_io(inputs), "flow_inputs.json")
                mlflow.log_dict(self._serialize_io(outputs), "flow_outputs.json")
            else:
                mlflow.log_dict(self._serialize_io(inputs), "flow_inputs.json")
                mlflow.log_dict(self._serialize_io(outputs), "flow_outputs.json")
            
            # Log cost summary
            if self._llm_cost_info:
                total_cost = sum(c['total_cost'] for c in self._llm_cost_info)
                total_input_tokens = sum(c['input_tokens'] for c in self._llm_cost_info)
                total_output_tokens = sum(c['output_tokens'] for c in self._llm_cost_info)
                total_tokens = sum(c['total_tokens'] for c in self._llm_cost_info)
                
                if self._custom_mlflow_client:
                    self._custom_mlflow_client.log_metric("total_cost", round(total_cost, 6))
                    self._custom_mlflow_client.log_metric("total_input_tokens", total_input_tokens)
                    self._custom_mlflow_client.log_metric("total_output_tokens", total_output_tokens)
                    self._custom_mlflow_client.log_metric("total_tokens", total_tokens)
                    # Use mlflow directly for log_dict since custom client doesn't have it
                    mlflow.log_dict(self._llm_cost_info, "llm_costs_details.json")
                else:
                    mlflow.log_metric("total_cost", round(total_cost, 6))
                    mlflow.log_metric("total_input_tokens", total_input_tokens)
                    mlflow.log_metric("total_output_tokens", total_output_tokens)
                    mlflow.log_metric("total_tokens", total_tokens)
                    mlflow.log_dict(self._llm_cost_info, "llm_costs_details.json")
            
            # Log overall metrics
            flow_data = self._flow_data.get(self._get_flow_key(), {})
            component_count = len(flow_data)
            success_components = sum(1 for c in flow_data.values() if c.get("success"))
            
            if self._custom_mlflow_client:
                self._custom_mlflow_client.log_metric("total_agent_duration_seconds", round(time.time() - self.start_time, 4))
                self._custom_mlflow_client.log_metric("component_count", component_count)
                self._custom_mlflow_client.log_metric("success_components", success_components)
                self._custom_mlflow_client.log_metric("error_components", component_count - success_components)
            else:
                mlflow.log_metric("total_agent_duration_seconds", round(time.time() - self.start_time, 4))
                mlflow.log_metric("component_count", component_count)
                mlflow.log_metric("success_components", success_components)
                mlflow.log_metric("error_components", component_count - success_components)
            
            # Log the trace tree structure
            trace_tree = self._build_trace_tree()
            if self._custom_mlflow_client:
                # Use mlflow directly for log_dict since custom client doesn't have it
                mlflow.log_dict(trace_tree, "trace_tree.json")
            else:
                mlflow.log_dict(trace_tree, "trace_tree.json")
            
            logger.info(f"✅ Successfully ended MLflow trace for flow {self.trace_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to end MLflow trace: {e}", exc_info=True)
        
        finally:
            # Don't end the run here - let MLflow autolog or user handle it
            self._cleanup_flow(self._get_flow_key())

    def _build_trace_tree(self) -> dict:
        """Build a tree structure of the trace for visualization."""
        flow_key = self._get_flow_key()
        flow_data = self._flow_data.get(flow_key, {})
        flow_order = self._flow_orders.get(flow_key, [])
        
        tree = {
            "name": self.trace_name,
            "type": self.trace_type,
            "trace_id": str(self.trace_id),
            "components": []
        }
        
        for trace_id in flow_order:
            component = flow_data.get(trace_id, {})
            tree["components"].append({
                "name": component.get("trace_name", "Unknown"),
                "type": component.get("trace_type", "Unknown"),
                "trace_id": trace_id,
                "success": component.get("success", False),
                "duration_seconds": component.get("duration_seconds", 0),
                "error": component.get("error")
            })
        
        return tree

    def _get_flow_key(self, trace_id: str = None) -> str:
        """Get flow key for data storage."""
        return str(self.trace_id)

    def _cleanup_flow(self, flow_key: str):
        """Clean up flow data."""
        self._flow_data.pop(flow_key, None)
        self._flow_orders.pop(flow_key, None)
        self._component_spans.clear()
        self._llm_cost_info.clear()
        self._root_span = None
        logger.debug(f"🧹 Cleaned up resources for flow {flow_key}")

    def _add_llm_cost_info(self, cost_info: Dict[str, Any]):
        """Add LLM cost information."""
        self._llm_cost_info.append(cost_info)

    def get_langchain_callback(self):
        """Get LangChain callback handler."""
        return self._callback_handler

    def _serialize_io(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure data is JSON serializable."""
        if not data:
            return {}
        try:
            json.dumps(data)
            return data
        except (TypeError, OverflowError):
            # Convert non-serializable objects to strings
            def make_serializable(obj):
                if isinstance(obj, dict):
                    return {k: make_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [make_serializable(item) for item in obj]
                elif isinstance(obj, (str, int, float, bool, type(None))):
                    return obj
                else:
                    return str(obj)
            
            return make_serializable(data)