"""
This module provides cost tracking functionality for LLM API usage.
It includes utilities for tracking, calculating and logging costs across
different model providers like OpenAI, Anthropic, Mistral etc.
"""

import json
import os
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional

import mlflow
import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

from ml_observability.utils import setup_logger

logger = setup_logger(__name__)

# Global thread pool for MLflow operations
_mlflow_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="mlflow-")

# Default cost rates per 1000 tokens (USD) as of April 2025.
# Prices are based on the provided pricing structure.
DEFAULT_COST_RATES = {
    # OpenAI Pricing
    "gpt-4o": {"input": 0.005, "output": 0.015, "provider": "OpenAI"},
    "gpt-4o-2024-08-06": {"input": 0.005, "output": 0.015, "provider": "OpenAI"},
    "gpt-4o-2024-05-13": {"input": 0.005, "output": 0.015, "provider": "OpenAI"},
    "gpt-4o-mini": {"input": 0.005, "output": 0.015, "provider": "OpenAI"},
    "gpt-4o-mini-2024-07-18": {"input": 0.005, "output": 0.015, "provider": "OpenAI"},
    "chatgpt-4o-latest": {"input": 0.005, "output": 0.015, "provider": "OpenAI"},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03, "provider": "OpenAI"},
    "gpt-4-turbo-2024-04-09": {"input": 0.01, "output": 0.03, "provider": "OpenAI"},
    "gpt-4": {"input": 0.03, "output": 0.06, "provider": "OpenAI"},
    "gpt-4-32k": {"input": 0.06, "output": 0.12, "provider": "OpenAI"},
    "gpt-4-0125-preview": {"input": 0.01, "output": 0.03, "provider": "OpenAI"},
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03, "provider": "OpenAI"},
    "gpt-4-vision-preview": {"input": 0.01, "output": 0.03, "provider": "OpenAI"},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015, "provider": "OpenAI"},
    "gpt-3.5-turbo-0125": {"input": 0.0005, "output": 0.0015, "provider": "OpenAI"},
    "gpt-3.5-turbo-instruct": {"input": 0.0015, "output": 0.002, "provider": "OpenAI"},
    "gpt-3.5-turbo-1106": {"input": 0.001, "output": 0.002, "provider": "OpenAI"},
    "gpt-3.5-turbo-0613": {"input": 0.0015, "output": 0.002, "provider": "OpenAI"},
    "gpt-3.5-turbo-16k-0613": {"input": 0.003, "output": 0.004, "provider": "OpenAI"},
    "gpt-3.5-turbo-0301": {"input": 0.0015, "output": 0.002, "provider": "OpenAI"},
    "davinci-002": {"input": 0.02, "output": 0.02, "provider": "OpenAI"},
    "babbage-002": {"input": 0.0004, "output": 0.0004, "provider": "OpenAI"},
    "o3-mini": {"input": 0.0005, "output": 0.0015, "provider": "OpenAI"},
    "o1-preview": {"input": 0.015, "output": 0.015, "provider": "OpenAI"},
    "o1": {"input": 0.015, "output": 0.015, "provider": "OpenAI"},
    "o1-mini": {"input": 0.015, "output": 0.015, "provider": "OpenAI"},
    "ft:gpt-3.5-turbo": {"input": 0.003, "output": 0.006, "provider": "OpenAI"},
    "text-davinci-003": {"input": 0.02, "output": 0.02, "provider": "OpenAI"},
    "whisper": {"input": 0.1, "output": 0, "provider": "OpenAI"},
    "tts-1-hd": {"input": 0.03, "output": 0, "provider": "OpenAI"},
    "tts-1": {"input": 0.015, "output": 0, "provider": "OpenAI"},
    # Anthropic Pricing
    "claude-3-5-sonnet-20240620": {
        "input": 0.003,
        "output": 0.015,
        "provider": "Anthropic",
    },
    "claude-3-7-sonnet-20250219": {
        "input": 0.003,
        "output": 0.015,
        "provider": "Anthropic",
    },
    "claude-3-opus-20240229": {
        "input": 0.015,
        "output": 0.075,
        "provider": "Anthropic",
    },
    "claude-3-sonnet-20240229": {
        "input": 0.003,
        "output": 0.075,
        "provider": "Anthropic",
    },
    "claude-3-haiku-20240307": {
        "input": 0.00025,
        "output": 0.00125,
        "provider": "Anthropic",
    },
    "claude-2.1": {"input": 0.008, "output": 0.024, "provider": "Anthropic"},
    "claude-2.0": {"input": 0.008, "output": 0.024, "provider": "Anthropic"},
    "claude-instant-1.2": {"input": 0.0008, "output": 0.0024, "provider": "Anthropic"},
    "anthropic-default": {"input": 0.008, "output": 0.024, "provider": "Anthropic"},
    "claude-instant-1": {"input": 0.0008, "output": 0.0024, "provider": "Anthropic"},
    "claude-instant-v1": {"input": 0.0008, "output": 0.0024, "provider": "Anthropic"},
    "claude-1": {"input": 0.008, "output": 0.024, "provider": "Anthropic"},
    "claude-v1": {"input": 0.008, "output": 0.024, "provider": "Anthropic"},
    "claude-v2": {"input": 0.008, "output": 0.024, "provider": "Anthropic"},
    "claude-3-opus": {"input": 0.015, "output": 0.075, "provider": "Anthropic"},
    "claude-3-sonnet": {"input": 0.003, "output": 0.075, "provider": "Anthropic"},
    "claude-3-haiku": {"input": 0.00025, "output": 0.00125, "provider": "Anthropic"},
    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015, "provider": "Anthropic"},
}


class CostTracker:
    """A class for tracking and managing costs associated with LLM API usage.

    This class provides functionality to:
    - Track costs for individual model inference requests
    - Support custom cost rates for different models
    - Load cost rates from environment variables or custom files
    - Calculate cost summaries across models and providers
    - Log cost metrics to MLflow for experiment tracking
    - Handle various model providers (OpenAI, Anthropic, Mistral, etc.)

    The costs are calculated based on input and output tokens using predefined
    or custom rates per 1000 tokens.
    """

    def __init__(
        self,
        cost_rates: Optional[Dict[str, Dict[str, float]]] = None,
        custom_rates_path: Optional[str] = None,
    ):
        self.cost_rates = DEFAULT_COST_RATES.copy()

        env_rates_path = os.getenv("MODELHUB_COST_RATES_PATH")
        if env_rates_path and os.path.exists(env_rates_path):
            self._load_rates_from_file(env_rates_path)
        if custom_rates_path and os.path.exists(custom_rates_path):
            self._load_rates_from_file(custom_rates_path)
        if cost_rates:
            self.cost_rates.update(cost_rates)

        self.tracked_costs: List[Dict[str, Any]] = []
        logger.debug(
            "CostTracker initialized with %d model rate configs", len(self.cost_rates)
        )

    def _load_rates_from_file(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                custom_rates = json.load(f)
            self.cost_rates.update(custom_rates)
            logger.debug("Loaded custom rates from %s", file_path)
        except (IOError, json.JSONDecodeError) as e:
            logger.error("Failed to load custom rates from %s: %s", file_path, str(e))

    def clean_model_name(self, name: str) -> str:
        """
        Normalize model names for cost lookup.
        This can include lowercasing, replacing common substrings,
        and stripping Azure-specific prefixes.
        """
        cleaned = name.lower().strip()
        # Replace common variations.
        cleaned = (
            cleaned.replace("gpt4", "gpt-4")
            .replace("gpt3", "gpt-3")
            .replace("gpt-35", "gpt-3.5")
        )
        cleaned = cleaned.replace("claude3", "claude-3").replace("claude2", "claude-2")
        # If using Azure, remove an 'azure-' prefix if present.
        if cleaned.startswith("azure-"):
            cleaned = cleaned[len("azure-") :]
        return cleaned

    def track_cost(
        self,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
        run_id: Optional[str] = None,
    ) -> float:
        """
        Track cost for a model call.

        Args:
            model_name: Name of the model
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            run_id: MLflow run ID (optional)

        Returns:
            Total cost for this call
        """
        logger.debug(f"Tracking cost for model {model_name}")
        logger.debug(f"Cost rates for {model_name}: {self.cost_rates}")
        logger.debug(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")

        # Get cost rates for the model
        rates = self.get_model_rates(model_name)

        # Calculate costs
        input_cost = (input_tokens / 1000) * rates["input"]
        output_cost = (output_tokens / 1000) * rates["output"]
        total_cost = input_cost + output_cost

        # Store the cost data
        cost_data = {
            "model": model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost,
            "provider": rates["provider"],
            "timestamp": datetime.now().isoformat(),
            "run_id": run_id,
        }

        self.tracked_costs.append(cost_data)

        # Log to MLflow immediately if we have a run_id
        if run_id:
            self._log_to_mlflow_immediately(cost_data, run_id)

        logger.debug(
            f"Tracked cost for {model_name}: ${total_cost:.4f} ({input_tokens} input, {output_tokens} output tokens)"
        )

        return total_cost

    def get_model_rates(self, model_name: str) -> Dict[str, float]:
        model_name = self.clean_model_name(model_name)
        if model_name in self.cost_rates:
            return self.cost_rates[model_name]
        for rate_model, rates in self.cost_rates.items():
            if model_name.startswith(rate_model):
                logger.debug(
                    "Using cost rates for %s as prefix match for %s",
                    rate_model,
                    model_name,
                )
                return rates
        logger.warning(
            "No cost rates found for model %s, using gpt-3.5-turbo rates as fallback",
            model_name,
        )
        return self.cost_rates.get("gpt-3.5-turbo", {"input": 0.5, "output": 1.5})

    def _guess_provider(self, model_name: str) -> str:
        model_name = model_name.lower()
        if model_name.startswith("gpt"):
            return "openai"
        elif model_name.startswith("claude"):
            return "anthropic"
        elif model_name.startswith("mistral"):
            return "mistral"
        elif model_name.startswith("llama"):
            return "meta"
        else:
            return "unknown"

    def _log_to_mlflow_immediately(self, cost_data: dict, run_id: str):
        """
        Schedule MLflow logging in background thread to avoid blocking LLM responses.
        """
        # Schedule MLflow operations in background thread
        _mlflow_executor.submit(self._log_to_mlflow_sync, cost_data, run_id)

    def _log_to_mlflow_sync(self, cost_data: dict, run_id: str):
        """
        Synchronous MLflow logging operations - runs in background thread.
        """
        try:
            import mlflow

            # Check if there's an active run with the same ID
            active_run = mlflow.active_run()
            if active_run and active_run.info.run_id == run_id:
                # We're in the same run, accumulate metrics
                self._accumulate_metrics_for_run_sync(cost_data, run_id)
            else:
                # Different run or no active run, log directly
                self._log_individual_metrics_sync(cost_data, run_id)

        except Exception as e:
            logger.warning(f"Failed to log cost data to MLflow: {e}")

    def _accumulate_metrics_for_run_sync(self, cost_data: dict, run_id: str):
        """
        Accumulate metrics for the current run - runs in background thread.
        """
        try:
            import mlflow

            # Use thread-safe operations for accumulator
            with threading.Lock():
                # Initialize run accumulator if not exists
                if not hasattr(self, "_run_accumulators"):
                    self._run_accumulators = {}

                if run_id not in self._run_accumulators:
                    self._run_accumulators[run_id] = {
                        "total_input_tokens": 0,
                        "total_output_tokens": 0,
                        "total_tokens": 0,
                        "total_input_cost": 0.0,
                        "total_output_cost": 0.0,
                        "total_cost": 0.0,
                        "call_count": 0,
                        "models_used": set(),
                        "providers_used": set(),
                    }

                # Accumulate values
                acc = self._run_accumulators[run_id]
                acc["total_input_tokens"] += cost_data["input_tokens"]
                acc["total_output_tokens"] += cost_data["output_tokens"]
                acc["total_tokens"] += cost_data["total_tokens"]
                acc["total_input_cost"] += cost_data["input_cost"]
                acc["total_output_cost"] += cost_data["output_cost"]
                acc["total_cost"] += cost_data["total_cost"]
                acc["call_count"] += 1
                acc["models_used"].add(cost_data["model"])
                acc["providers_used"].add(cost_data["provider"])

            # Log accumulated metrics to MLflow (outside the lock)
            mlflow.log_metrics(
                {
                    "total_input_tokens": acc["total_input_tokens"],
                    "total_output_tokens": acc["total_output_tokens"],
                    "total_tokens": acc["total_tokens"],
                    "total_input_cost": acc["total_input_cost"],
                    "total_output_cost": acc["total_output_cost"],
                    "total_cost": acc["total_cost"],
                    "llm_call_count": acc["call_count"],
                }
            )

            # Log parameters (will not overwrite if already set)
            mlflow.log_params(
                {
                    "models_used": ",".join(sorted(acc["models_used"])),
                    "providers_used": ",".join(sorted(acc["providers_used"])),
                }
            )

            logger.debug(
                f"Accumulated metrics for run {run_id}: {acc['call_count']} calls, ${acc['total_cost']:.4f} total cost"
            )

        except Exception as e:
            logger.warning(f"Failed to accumulate metrics for run {run_id}: {e}")

    def _log_individual_metrics_sync(self, cost_data: dict, run_id: str):
        """
        Log individual metrics - runs in background thread.
        """
        try:
            import mlflow

            # Use the existing run context or start a temporary one
            with mlflow.start_run(run_id=run_id):
                mlflow.log_metrics(
                    {
                        "input_tokens": cost_data["input_tokens"],
                        "output_tokens": cost_data["output_tokens"],
                        "total_tokens": cost_data["total_tokens"],
                        "input_cost": cost_data["input_cost"],
                        "output_cost": cost_data["output_cost"],
                        "total_cost": cost_data["total_cost"],
                    }
                )

                mlflow.log_params(
                    {
                        "model": cost_data["model"],
                        "provider": cost_data["provider"],
                    }
                )

            logger.debug(f"Logged individual metrics for run {run_id}")

        except Exception as e:
            logger.warning(f"Failed to log individual metrics for run {run_id}: {e}")

    # Backward compatibility methods
    def _accumulate_metrics_for_run(self, cost_data: dict, run_id: str):
        """Deprecated - use _accumulate_metrics_for_run_sync instead"""
        return self._accumulate_metrics_for_run_sync(cost_data, run_id)

    def _log_individual_metrics(self, cost_data: dict, run_id: str):
        """Deprecated - use _log_individual_metrics_sync instead"""
        return self._log_individual_metrics_sync(cost_data, run_id)

    def get_cost_summary(self) -> Dict[str, Any]:
        """Get a summary of all tracked costs.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - total_cost: Total cost across all requests
                - total_requests: Number of tracked requests
                - total_tokens: Total tokens processed
                - models: Dictionary of per-model statistics including:
                    - total_cost, input_tokens, output_tokens
                    - total_tokens, number of requests
                - providers: Dictionary of per-provider statistics including:
                    - total_cost, input_tokens, output_tokens
                    - total_tokens, number of requests
        """
        if not self.tracked_costs:
            return {
                "total_cost": 0.0,
                "total_requests": 0,
                "total_tokens": 0,
                "models": {},
                "providers": {},
            }
        df = pd.DataFrame(self.tracked_costs)
        total_cost = df["total_cost"].sum()
        total_requests = len(df)
        total_tokens = df["total_tokens"].sum()
        model_costs = (
            df.groupby("model")
            .agg(
                {
                    "total_cost": "sum",
                    "input_tokens": "sum",
                    "output_tokens": "sum",
                    "total_tokens": "sum",
                    "timestamp": "count",
                }
            )
            .rename(columns={"timestamp": "requests"})
            .to_dict(orient="index")
        )
        provider_costs = (
            df.groupby("provider")
            .agg(
                {
                    "total_cost": "sum",
                    "input_tokens": "sum",
                    "output_tokens": "sum",
                    "total_tokens": "sum",
                    "timestamp": "count",
                }
            )
            .rename(columns={"timestamp": "requests"})
            .to_dict(orient="index")
        )
        return {
            "total_cost": total_cost,
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "models": model_costs,
            "providers": provider_costs,
        }

    def log_cost_summary_to_mlflow(self):
        """Log a summary of all tracked costs to MLflow.

        This method creates and logs several artifacts to MLflow including:
        - CSV files with cost breakdowns by model and provider
        - A detailed CSV of all tracked costs
        - A JSON summary of aggregate statistics
        - Key metrics for total cost, requests, and tokens

        """
        if not self.tracked_costs:
            logger.info("No costs to log")
            return
        summary = self.get_cost_summary()
        try:
            models_df = []
            for model_name, stats in summary["models"].items():
                models_df.append(
                    {
                        "model": model_name,
                        "requests": stats["requests"],
                        "total_tokens": stats["total_tokens"],
                        "input_tokens": stats["input_tokens"],
                        "output_tokens": stats["output_tokens"],
                        "total_cost": stats["total_cost"],
                    }
                )
            models_df = pd.DataFrame(models_df)

            providers_df = []
            for provider_name, stats in summary["providers"].items():
                providers_df.append(
                    {
                        "provider": provider_name,
                        "requests": stats["requests"],
                        "total_tokens": stats["total_tokens"],
                        "input_tokens": stats["input_tokens"],
                        "output_tokens": stats["output_tokens"],
                        "total_cost": stats["total_cost"],
                    }
                )
            providers_df = pd.DataFrame(providers_df)

            with tempfile.TemporaryDirectory() as tmp_dir:
                model_summary_path = os.path.join(tmp_dir, "cost_summary_by_model.csv")
                models_df.to_csv(model_summary_path, index=False)
                provider_summary_path = os.path.join(
                    tmp_dir, "cost_summary_by_provider.csv"
                )
                providers_df.to_csv(provider_summary_path, index=False)
                details_path = os.path.join(tmp_dir, "cost_details.csv")
                pd.DataFrame(self.tracked_costs).to_csv(details_path, index=False)
                json_path = os.path.join(tmp_dir, "cost_summary.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(summary, f, indent=2)
                mlflow.log_artifact(model_summary_path, "cost_tracking")
                mlflow.log_artifact(provider_summary_path, "cost_tracking")
                mlflow.log_artifact(details_path, "cost_tracking")
                mlflow.log_artifact(json_path, "cost_tracking")
                mlflow.log_metric("llm_cost_summary_total", summary["total_cost"])
                mlflow.log_metric(
                    "llm_cost_summary_requests", summary["total_requests"]
                )
                mlflow.log_metric("llm_cost_summary_tokens", summary["total_tokens"])
                logger.info(
                    "Logged cost summary to MLflow: $%.4f for %d requests (%d tokens)",
                    summary["total_cost"],
                    summary["total_requests"],
                    summary["total_tokens"],
                )
        except (IOError, ValueError, mlflow.exceptions.MlflowException) as e:
            logger.warning("Failed to log cost summary to MLflow: %s", str(e))

    def reset(self):
        """Reset the cost tracker by clearing all tracked costs.

        This method clears the internal list of tracked costs, effectively
        resetting the tracker to its initial state. All previously tracked
        costs will be removed.
        """
        self.tracked_costs = []
