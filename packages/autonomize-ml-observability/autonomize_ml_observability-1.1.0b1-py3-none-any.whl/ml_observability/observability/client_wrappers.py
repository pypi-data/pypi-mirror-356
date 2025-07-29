# NEW FILE: ml_observability/observability/client_wrappers.py
import asyncio
import functools
import time
from typing import Any, Callable
import inspect

from ml_observability.observability.async_monitor import _monitor
from ml_observability.utils import setup_logger

logger = setup_logger(__name__)


def wrap_openai_async(client):
    """Wrap OpenAI client for non-blocking monitoring."""

    # Wrap async completions
    if hasattr(client.chat, "completions") and hasattr(
        client.chat.completions, "create"
    ):
        original_create = client.chat.completions.create

        @functools.wraps(original_create)
        async def wrapped_create(*args, **kwargs):
            start_time = time.time()
            call_id = str(time.time())  # Simple unique ID

            # Fire and forget - track start without waiting
            asyncio.create_task(
                _monitor.track_llm_start(
                    call_id=call_id,
                    model=kwargs.get("model", "gpt-3.5-turbo"),
                    provider="openai",
                    params={
                        k: v
                        for k, v in kwargs.items()
                        if k not in ["messages", "api_key"]
                    },
                )
            )

            error = None
            result = None

            try:
                # Make the actual API call
                result = await original_create(*args, **kwargs)
                return result

            except Exception as e:
                error = e
                raise

            finally:
                # Fire and forget - track end without waiting
                duration_ms = (time.time() - start_time) * 1000

                end_event = {
                    "call_id": call_id,
                    "duration_ms": duration_ms,
                    "error": str(error) if error else None,
                    "model": kwargs.get("model", "gpt-3.5-turbo"),
                }

                if result and hasattr(result, "usage"):
                    end_event["usage"] = {
                        "prompt_tokens": result.usage.prompt_tokens,
                        "completion_tokens": result.usage.completion_tokens,
                        "total_tokens": result.usage.total_tokens,
                    }

                asyncio.create_task(_monitor.track_llm_end(**end_event))

        client.chat.completions.create = wrapped_create

    logger.debug("Async non-blocking monitoring enabled for OpenAI client")


def wrap_openai_sync(client):
    """Wrap sync OpenAI client for non-blocking monitoring."""

    if hasattr(client.chat, "completions") and hasattr(
        client.chat.completions, "create"
    ):
        original_create = client.chat.completions.create

        @functools.wraps(original_create)
        def wrapped_create(*args, **kwargs):
            start_time = time.time()
            call_id = str(time.time())

            # Track start without blocking
            _monitor.track_sync(
                {
                    "type": "llm_start",
                    "call_id": call_id,
                    "model": kwargs.get("model", "gpt-3.5-turbo"),
                    "provider": "openai",
                    "params": {
                        k: v
                        for k, v in kwargs.items()
                        if k not in ["messages", "api_key"]
                    },
                }
            )

            error = None
            result = None

            try:
                result = original_create(*args, **kwargs)
                return result

            except Exception as e:
                error = e
                raise

            finally:
                duration_ms = (time.time() - start_time) * 1000

                end_event = {
                    "type": "llm_end",
                    "call_id": call_id,
                    "duration_ms": duration_ms,
                    "error": str(error) if error else None,
                    "model": kwargs.get("model", "gpt-3.5-turbo"),
                }

                if result and hasattr(result, "usage"):
                    end_event["usage"] = {
                        "prompt_tokens": result.usage.prompt_tokens,
                        "completion_tokens": result.usage.completion_tokens,
                        "total_tokens": result.usage.total_tokens,
                    }

                _monitor.track_sync(end_event)

        client.chat.completions.create = wrapped_create


def wrap_anthropic_async(client):
    """Wrap Anthropic client for non-blocking monitoring."""

    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        original_create = client.messages.create

        @functools.wraps(original_create)
        async def wrapped_create(*args, **kwargs):
            start_time = time.time()
            call_id = str(time.time())

            # Fire and forget tracking
            asyncio.create_task(
                _monitor.track_llm_start(
                    call_id=call_id,
                    model=kwargs.get("model", "claude-2"),
                    provider="anthropic",
                    params={
                        k: v
                        for k, v in kwargs.items()
                        if k not in ["messages", "api_key"]
                    },
                )
            )

            error = None
            result = None

            try:
                result = await original_create(*args, **kwargs)
                return result

            except Exception as e:
                error = e
                raise

            finally:
                duration_ms = (time.time() - start_time) * 1000

                end_event = {
                    "call_id": call_id,
                    "duration_ms": duration_ms,
                    "error": str(error) if error else None,
                    "model": kwargs.get("model", "claude-2"),
                }

                if result and hasattr(result, "usage"):
                    end_event["usage"] = {
                        "prompt_tokens": result.usage.input_tokens,
                        "completion_tokens": result.usage.output_tokens,
                        "total_tokens": result.usage.input_tokens
                        + result.usage.output_tokens,
                    }

                asyncio.create_task(_monitor.track_llm_end(**end_event))

        client.messages.create = wrapped_create


def wrap_anthropic_sync(client):
    """Wrap sync Anthropic client for non-blocking monitoring."""

    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        original_create = client.messages.create

        @functools.wraps(original_create)
        def wrapped_create(*args, **kwargs):
            start_time = time.time()
            call_id = str(time.time())

            # Track start without blocking
            _monitor.track_sync(
                {
                    "type": "llm_start",
                    "call_id": call_id,
                    "model": kwargs.get("model", "claude-2"),
                    "provider": "anthropic",
                    "params": {
                        k: v
                        for k, v in kwargs.items()
                        if k not in ["messages", "api_key"]
                    },
                }
            )

            error = None
            result = None

            try:
                result = original_create(*args, **kwargs)
                return result

            except Exception as e:
                error = e
                raise

            finally:
                duration_ms = (time.time() - start_time) * 1000

                end_event = {
                    "type": "llm_end",
                    "call_id": call_id,
                    "duration_ms": duration_ms,
                    "error": str(error) if error else None,
                    "model": kwargs.get("model", "claude-2"),
                }

                if result and hasattr(result, "usage"):
                    end_event["usage"] = {
                        "prompt_tokens": result.usage.input_tokens,
                        "completion_tokens": result.usage.output_tokens,
                        "total_tokens": result.usage.input_tokens
                        + result.usage.output_tokens,
                    }

                _monitor.track_sync(end_event)

        client.messages.create = wrapped_create
