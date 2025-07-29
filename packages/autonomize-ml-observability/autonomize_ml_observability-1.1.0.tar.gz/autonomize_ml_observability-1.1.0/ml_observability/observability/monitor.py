"""
This module provides monitoring and observability capabilities for LLM (Large Language Model)
clients.
It includes functionality for cost tracking, MLflow integration, and client wrapping for various
LLM providers like OpenAI, Azure OpenAI, and Anthropic.
"""

import os
import logging
from typing import Optional, Any
import asyncio
import inspect
import time
import functools
import threading
import uuid

import mlflow

from autonomize.core.credential import ModelhubCredential
from ..core.exceptions import ModelhubMissingCredentialsException
from ..utils import setup_logger
from ml_observability.observability.cost_tracking import CostTracker
from ml_observability.core.mlflow_client import MLflowClient

# NEW IMPORTS
from ml_observability.observability.async_monitor import (
    initialize_async,
    _monitor as async_monitor,
)
from ml_observability.observability.client_wrappers import (
    wrap_openai_async,
    wrap_openai_sync,
    wrap_anthropic_async,
    wrap_anthropic_sync,
)

logger = logging.getLogger(__name__)

# Global instances
_mlflow_client: Optional[MLflowClient] = None
_cost_tracker: CostTracker
_initialized: bool = False  # NEW: Global initialization flag

# Add thread-local storage for run management
_local = threading.local()


def initialize(
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[ModelhubCredential] = None,
):
    """
    Initialize the MLflowClient, Observability, and CostTracker.
    Must be called once at startup.

    Args:
        cost_rates (dict, optional): Dictionary of cost rates for different models
        experiment_name (str, optional): Name of the MLflow experiment
        credential (ModelhubCredential, optional): Modelhub credentials
    """
    global _mlflow_client, _cost_tracker, _initialized

    # Check if already initialized
    if _initialized:
        logger.debug("Observability system already initialized, skipping.")
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
            credential = ModelhubCredential(
                modelhub_url=os.getenv("MODELHUB_BASE_URL"),
                client_id=os.getenv("MODELHUB_CLIENT_ID"),
                client_secret=os.getenv("MODELHUB_CLIENT_SECRET"),
            )

        _mlflow_client = MLflowClient(
            credential=credential,
        )

    experiment_name = experiment_name or os.getenv("EXPERIMENT_NAME")
    if experiment_name:
        if _mlflow_client:
            _mlflow_client.set_experiment(experiment_name=experiment_name)
        else:
            mlflow.set_experiment(experiment_name)
    _cost_tracker = CostTracker(cost_rates=cost_rates)

    # Mark as initialized
    _initialized = True
    logger.debug("Observability system initialized.")


def monitor(
    client,
    provider: Optional[str] = None,
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[ModelhubCredential] = None,
    # NEW PARAMETER
    use_async: bool = True,  # Default to async non-blocking monitoring
):
    """
    Enable monitoring on an LLM client.
    Supports multiple providers: 'openai', 'azure_openai', 'anthropic', etc.
    If provider is not provided, it is inferred from the client's module.

    Args:
        client: The LLM client to monitor
        provider (str, optional): The provider name (openai, azure_openai, anthropic)
        cost_rates (dict, optional): Dictionary of cost rates for different models
        experiment_name (str, optional): Name of the MLflow experiment
        credential (ModelhubCredential, optional): Modelhub credentials
        use_async (bool, optional): Use async non-blocking monitoring (default: True)
    """
    # ALWAYS initialize first - this sets up MLflow client and cost tracker
    # But only if not already initialized
    initialize(
        cost_rates=cost_rates,
        experiment_name=experiment_name,
        credential=credential,
    )

    # Check if we should use async monitoring
    if use_async:
        return _monitor_async(client, provider, cost_rates, experiment_name, credential)

    # Original synchronous monitoring code (initialize already called above)
    if provider is None:
        # Try checking the class name first.
        client_name = client.__class__.__name__.lower()
        if "azure" in client_name:
            provider = "azure_openai"
        elif "openai" in client_name:
            provider = "openai"
        elif "anthropic" in client_name:
            provider = "anthropic"
        else:
            # Fallback to module-based detection.
            mod = client.__class__.__module__.lower()
            if "openai" in mod:
                provider = "openai"
            elif "azure" in mod:
                provider = "azure_openai"
            elif "anthropic" in mod:
                provider = "anthropic"
            else:
                provider = "unknown"

    logger.debug("Detected provider: %s", provider)

    if provider in ("openai", "azure_openai"):
        if _mlflow_client:
            _mlflow_client.mlflow.openai.autolog()
        else:
            mlflow.openai.autolog()
        wrap_openai(client)
    elif provider == "anthropic":
        if _mlflow_client:
            _mlflow_client.mlflow.anthropic.autolog()
        else:
            mlflow.anthropic.autolog()
        wrap_anthropic(client)
    else:
        logger.warning("Monitoring not implemented for provider %s", provider)


# NEW FUNCTION: Async monitoring
def _monitor_async(
    client,
    provider: Optional[str] = None,
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[Any] = None,
):
    """
    Enable async non-blocking monitoring on an LLM client.
    """
    # Auto-detect provider
    if provider is None:
        client_module = client.__class__.__module__.lower()
        client_name = client.__class__.__name__.lower()

        if "openai" in client_module or "openai" in client_name:
            provider = "openai"
        elif "anthropic" in client_module or "anthropic" in client_name:
            provider = "anthropic"
        else:
            logger.warning(f"Unknown provider for client {client.__class__.__name__}")
            return client

    # ENABLE AUTOLOG FOR ASYNC MONITORING TOO
    logger.debug("Enabling MLflow autolog for async monitoring")
    if provider in ("openai", "azure_openai"):
        if _mlflow_client:
            _mlflow_client.mlflow.openai.autolog()
        else:
            mlflow.openai.autolog()
    elif provider == "anthropic":
        if _mlflow_client:
            _mlflow_client.mlflow.anthropic.autolog()
        else:
            mlflow.anthropic.autolog()

    # Initialize async monitor if needed (but don't duplicate main initialization)
    if not async_monitor._initialized:
        # Run initialization in background
        loop = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop, create one for initialization
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # Schedule initialization
            asyncio.create_task(
                initialize_async(cost_rates=cost_rates, experiment_name=experiment_name)
            )
        else:
            # Run initialization
            loop.run_until_complete(
                initialize_async(cost_rates=cost_rates, experiment_name=experiment_name)
            )

    # Detect if client is async
    is_async_client = any(
        asyncio.iscoroutinefunction(getattr(client, method, None))
        for method in ["create", "acreate", "__call__"]
    )

    # Wrap based on provider and sync/async - but with separate runs
    if provider == "openai":
        if is_async_client or "async" in client.__class__.__name__.lower():
            wrap_openai_async_with_separate_runs(client)
        else:
            wrap_openai_sync_with_separate_runs(client)

    elif provider == "anthropic":
        if is_async_client or "async" in client.__class__.__name__.lower():
            wrap_anthropic_async_with_separate_runs(client)
        else:
            wrap_anthropic_sync_with_separate_runs(client)

    logger.debug(f"Non-blocking monitoring enabled for {provider} client")
    return client


def wrap_openai_async_with_separate_runs(client):
    """Wrap OpenAI async client with separate runs for each LLM call."""
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        if (
            hasattr(client.chat.completions, "create")
            and callable(client.chat.completions.create)
            and client.__class__.__name__ == "AsyncOpenAI"
        ):
            original_async_create = client.chat.completions.create

            async def wrapped_async_create(*args, **kwargs):
                # Check if MLflow autolog is handling the run
                active_run = mlflow.active_run()
                should_manage_run = active_run is None

                if should_manage_run:
                    # Only create our own run if MLflow autolog isn't managing one
                    run_name = f"async_llm_call_{uuid.uuid4().hex[:8]}"
                    run = mlflow.start_run(run_name=run_name)
                else:
                    run = active_run

                try:
                    result = await original_async_create(*args, **kwargs)

                    # Track cost regardless of who manages the run
                    if hasattr(result, "usage") and result.usage:
                        prompt_tokens = result.usage.prompt_tokens
                        completion_tokens = result.usage.completion_tokens
                        _cost_tracker.track_cost(
                            model_name=kwargs.get("model", "gpt-3.5-turbo"),
                            input_tokens=prompt_tokens,
                            output_tokens=completion_tokens,
                            run_id=run.info.run_id,
                        )

                    # Log model parameter only if we're managing the run
                    if should_manage_run:
                        if _mlflow_client:
                            _mlflow_client.log_param(
                                "model", kwargs.get("model", "gpt-3.5-turbo")
                            )
                        else:
                            mlflow.log_param(
                                "model", kwargs.get("model", "gpt-3.5-turbo")
                            )

                    return result
                finally:
                    # Only end the run if we started it
                    if should_manage_run:
                        mlflow.end_run()

            client.chat.completions.create = wrapped_async_create


def wrap_openai_sync_with_separate_runs(client):
    """Wrap OpenAI sync client with separate runs for each LLM call."""
    if hasattr(client.chat, "completions") and hasattr(
        client.chat.completions, "create"
    ):
        original_create = client.chat.completions.create

        def wrapped_create(*args, **kwargs):
            # Check if MLflow autolog is handling the run
            active_run = mlflow.active_run()
            should_manage_run = active_run is None

            if should_manage_run:
                # Only create our own run if MLflow autolog isn't managing one
                run_name = f"llm_call_{uuid.uuid4().hex[:8]}"
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run

            try:
                result = original_create(*args, **kwargs)

                # Track cost regardless of who manages the run
                if hasattr(result, "usage") and result.usage:
                    prompt_tokens = result.usage.prompt_tokens
                    completion_tokens = result.usage.completion_tokens
                    _cost_tracker.track_cost(
                        model_name=kwargs.get("model", "gpt-3.5-turbo"),
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id,
                    )

                # Log model parameter only if we're managing the run
                if should_manage_run:
                    if _mlflow_client:
                        _mlflow_client.log_param(
                            "model", kwargs.get("model", "gpt-3.5-turbo")
                        )
                    else:
                        mlflow.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))

                return result
            finally:
                # Only end the run if we started it
                if should_manage_run:
                    mlflow.end_run()

        client.chat.completions.create = wrapped_create


def wrap_anthropic_async_with_separate_runs(client):
    """Wrap Anthropic async client with separate runs for each LLM call."""
    if hasattr(client, "messages") and hasattr(client.messages, "acreate"):
        original_acreate = client.messages.acreate

        async def wrapped_acreate(*args, **kwargs):
            # Check if MLflow autolog is handling the run
            active_run = mlflow.active_run()
            should_manage_run = active_run is None

            if should_manage_run:
                # Only create our own run if MLflow autolog isn't managing one
                run_name = f"async_anthropic_call_{uuid.uuid4().hex[:8]}"
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run

            try:
                result = await original_acreate(*args, **kwargs)

                # Track cost regardless of who manages the run
                if hasattr(result, "usage") and result.usage:
                    prompt_tokens = result.usage.input_tokens
                    completion_tokens = result.usage.output_tokens
                    _cost_tracker.track_cost(
                        model_name=kwargs.get("model", "anthropic-default"),
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id,
                    )

                # Log model parameter only if we're managing the run
                if should_manage_run:
                    if _mlflow_client:
                        _mlflow_client.log_param(
                            "model", kwargs.get("model", "anthropic-default")
                        )
                    else:
                        mlflow.log_param(
                            "model", kwargs.get("model", "anthropic-default")
                        )

                return result
            finally:
                # Only end the run if we started it
                if should_manage_run:
                    mlflow.end_run()

        client.messages.acreate = wrapped_acreate


def wrap_anthropic_sync_with_separate_runs(client):
    """Wrap Anthropic sync client with separate runs for each LLM call."""
    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        original_create = client.messages.create

        def wrapped_create(*args, **kwargs):
            # Check if MLflow autolog is handling the run
            active_run = mlflow.active_run()
            should_manage_run = active_run is None

            if should_manage_run:
                # Only create our own run if MLflow autolog isn't managing one
                run_name = f"anthropic_call_{uuid.uuid4().hex[:8]}"
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run

            try:
                result = original_create(*args, **kwargs)

                # Track cost regardless of who manages the run
                if hasattr(result, "usage") and result.usage:
                    prompt_tokens = result.usage.input_tokens
                    completion_tokens = result.usage.output_tokens
                    _cost_tracker.track_cost(
                        model_name=kwargs.get("model", "anthropic-default"),
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id,
                    )

                # Log model parameter only if we're managing the run
                if should_manage_run:
                    if _mlflow_client:
                        _mlflow_client.log_param(
                            "model", kwargs.get("model", "anthropic-default")
                        )
                    else:
                        mlflow.log_param(
                            "model", kwargs.get("model", "anthropic-default")
                        )

                return result
            finally:
                # Only end the run if we started it
                if should_manage_run:
                    mlflow.end_run()

        client.messages.create = wrapped_create


# NEW DECORATORS
def trace_async(name: Optional[str] = None):
    """Decorator for async functions with non-blocking tracing."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            func_name = name or func.__name__

            # Track start without blocking
            asyncio.create_task(
                async_monitor.track_component_start(
                    name=func_name, component_type="function"
                )
            )

            error = None
            result = None

            try:
                result = await func(*args, **kwargs)
                return result

            except Exception as e:
                error = e
                raise

            finally:
                duration_ms = (time.time() - start_time) * 1000

                # Track end without blocking
                asyncio.create_task(
                    async_monitor.track_component_end(
                        name=func_name,
                        duration_ms=duration_ms,
                        error=str(error) if error else None,
                        outputs={"result": str(result)[:100]} if result else None,
                    )
                )

        return wrapper

    return decorator


def trace_sync(name: Optional[str] = None):
    """Decorator for sync functions with non-blocking tracing."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func_name = name or func.__name__

            # Track start without blocking
            async_monitor.track_sync(
                {
                    "type": "component_start",
                    "name": func_name,
                    "component_type": "function",
                }
            )

            error = None
            result = None

            try:
                result = func(*args, **kwargs)
                return result

            except Exception as e:
                error = e
                raise

            finally:
                duration_ms = (time.time() - start_time) * 1000

                # Track end without blocking
                async_monitor.track_sync(
                    {
                        "type": "component_end",
                        "name": func_name,
                        "duration_ms": duration_ms,
                        "error": str(error) if error else None,
                        "outputs": {"result": str(result)[:100]} if result else None,
                    }
                )

        return wrapper

    return decorator


def wrap_openai(client):
    """
    Wraps an OpenAI client to enable monitoring and logging capabilities.

    This function intercepts the client's completion creation methods (both synchronous
    and asynchronous) to track costs, log parameters, and manage MLflow runs.

    Args:
        client: An instance of the OpenAI client to be wrapped.

    Returns:
        None. The function modifies the client instance in-place by wrapping its methods.
    """
    # Wrap synchronous completions.create
    if hasattr(client.chat, "completions") and hasattr(
        client.chat.completions, "create"
    ):
        original_create = client.chat.completions.create

        def wrapped_create(*args, **kwargs):
            active = mlflow.active_run()
            logger.debug("Active run: %s", active)
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = original_create(*args, **kwargs)
                logger.debug("result: %s", result)
                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "gpt-3.5-turbo"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id,
                )
                if _mlflow_client:
                    _mlflow_client.log_param(
                        "model", kwargs.get("model", "gpt-3.5-turbo")
                    )
                else:
                    mlflow.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.chat.completions.create = wrapped_create

    # Wrap asynchronous completions.create (create)
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        # Check if the client is an AsyncOpenAI instance
        if (
            hasattr(client.chat.completions, "create")
            and callable(client.chat.completions.create)
            and client.__class__.__name__ == "AsyncOpenAI"
        ):
            original_async_create = client.chat.completions.create

            async def wrapped_async_create(*args, **kwargs):
                active = mlflow.active_run()
                logger.debug("Active async run: %s", active)
                started_run = False
                if not active:
                    run = mlflow.start_run(run_name="async_llm_call_auto")
                    started_run = True
                else:
                    run = active

                try:
                    result = original_async_create(*args, **kwargs)
                    prompt_tokens = result.usage.prompt_tokens
                    completion_tokens = result.usage.completion_tokens
                    _cost_tracker.track_cost(
                        model_name=kwargs.get("model", "gpt-3.5-turbo"),
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id,
                    )
                    if _mlflow_client:
                        _mlflow_client.log_param(
                            "model", kwargs.get("model", "gpt-3.5-turbo")
                        )
                    else:
                        mlflow.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                    return result
                finally:
                    if started_run:
                        mlflow.end_run()

            client.chat.completions.create = wrapped_async_create

    logger.debug("Monitoring enabled for OpenAI/AzureOpenAI client.")


def wrap_anthropic(client):
    """
    Wraps an Anthropic client to enable monitoring and logging capabilities.

    This function intercepts the client's message creation methods (both synchronous
    and asynchronous) to track costs, log parameters, and manage MLflow runs.

    Args:
        client: An instance of the Anthropic client to be wrapped.

    Returns:
        None. The function modifies the client instance in-place by wrapping its methods.
    """
    # Wrap synchronous messages.create.
    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        original_create = client.messages.create

        def wrapped_create(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = original_create(*args, **kwargs)
                prompt_tokens = result.usage.input_tokens
                completion_tokens = result.usage.output_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "anthropic-default"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id,
                )
                if _mlflow_client:
                    _mlflow_client.log_param(
                        "model", kwargs.get("model", "anthropic-default")
                    )
                else:
                    mlflow.log_param("model", kwargs.get("model", "anthropic-default"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.messages.create = wrapped_create

    # Wrap asynchronous messages.acreate if available.
    if hasattr(client, "messages") and hasattr(client.messages, "acreate"):
        original_acreate = client.messages.acreate

        async def wrapped_acreate(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = await original_acreate(*args, **kwargs)
                prompt_tokens = result.usage.input_tokens
                completion_tokens = result.usage.output_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "anthropic-default"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id,
                )
                if _mlflow_client:
                    _mlflow_client.log_param(
                        "model", kwargs.get("model", "anthropic-default")
                    )
                else:
                    mlflow.log_param("model", kwargs.get("model", "anthropic-default"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.messages.acreate = wrapped_acreate

    logger.debug("Monitoring enabled for Anthropics client.")


def agent(name=None):
    """
    Decorator for agent functions.
    Automatically wraps the function execution in an MLflow run.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                mlflow.start_run(run_name=name or fn.__name__)
                started_run = True
            else:
                run = active
            try:
                return fn(*args, **kwargs)
            finally:
                if started_run:
                    mlflow.end_run()

        return wrapper

    return decorator


def tool(name=None):
    """
    Decorator for tool functions.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name=name or fn.__name__)
                started_run = True
            else:
                run = active
            try:
                return fn(*args, **kwargs)
            finally:
                if started_run:
                    mlflow.end_run()

        return wrapper

    return decorator


class Identify:
    """
    A simple context manager for setting user context (if needed).
    """

    def __init__(self, user_props=None):
        self.user_props = user_props

    def __enter__(self):
        # Set user context here if desired.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clear user context.
        pass


def identify(user_props=None):
    """
    Creates and returns an Identify context manager for setting user context.

    Args:
        user_props (dict, optional): Dictionary containing user properties to be set
            during the context. Defaults to None.

    Returns:
        Identify: A context manager instance that handles user context.
    """
    return Identify(user_props)
