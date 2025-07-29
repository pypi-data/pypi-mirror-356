import asyncio
import atexit
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional, Callable
import functools
import mlflow
from datetime import datetime
import uuid
from queue import Queue, Empty
import json

from ml_observability.observability.cost_tracking import CostTracker
from ml_observability.utils import setup_logger

logger = setup_logger(__name__)


class AsyncMonitor:
    """
    Async monitor that processes all tracking in background without blocking LLM calls.
    """

    def __init__(self):
        self.cost_tracker = CostTracker()
        self.event_queue = asyncio.Queue(maxsize=10000)
        self.sync_queue = Queue(maxsize=10000)
        self.worker_task = None
        self.sync_worker_thread = None
        self.executor = ThreadPoolExecutor(
            max_workers=4, thread_name_prefix="mlflow_worker"
        )
        self.running = False
        self._initialized = False

        # Register cleanup
        atexit.register(self.cleanup)

    async def initialize(self, experiment_name: Optional[str] = None):
        """Initialize the async monitor."""
        if self._initialized:
            return

        if experiment_name:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, mlflow.set_experiment, experiment_name
            )

        self.running = True
        self.worker_task = asyncio.create_task(self._async_worker())
        self.sync_worker_thread = threading.Thread(
            target=self._sync_worker, daemon=True
        )
        self.sync_worker_thread.start()
        self._initialized = True
        logger.debug("Async monitor initialized")

    async def _async_worker(self):
        """Background worker to process async events."""
        while self.running:
            try:
                # Process events in batches for efficiency
                events = []

                # Collect up to 10 events or wait 0.1 seconds
                try:
                    for _ in range(10):
                        event = await asyncio.wait_for(
                            self.event_queue.get(), timeout=0.1
                        )
                        events.append(event)
                except asyncio.TimeoutError:
                    pass

                if events:
                    # Process events in thread pool to not block async loop
                    await asyncio.get_event_loop().run_in_executor(
                        self.executor, self._process_events, events
                    )

            except Exception as e:
                logger.error(f"Error in async worker: {e}")
                await asyncio.sleep(1)  # Prevent tight loop on errors

    def _sync_worker(self):
        """Background worker for sync events."""
        while self.running:
            try:
                events = []
                # Batch process sync events
                deadline = datetime.utcnow().timestamp() + 0.1

                while datetime.utcnow().timestamp() < deadline:
                    try:
                        event = self.sync_queue.get(timeout=0.01)
                        events.append(event)
                        if len(events) >= 10:
                            break
                    except Empty:
                        break

                if events:
                    self._process_events(events)

            except Exception as e:
                logger.error(f"Error in sync worker: {e}")

    def _process_events(self, events: list):
        """Process a batch of events."""
        for event in events:
            try:
                event_type = event.get("type")

                if event_type == "llm_start":
                    self._handle_llm_start(event)
                elif event_type == "llm_end":
                    self._handle_llm_end(event)
                elif event_type == "component_start":
                    self._handle_component_start(event)
                elif event_type == "component_end":
                    self._handle_component_end(event)
                elif event_type == "metric":
                    self._handle_metric(event)

            except Exception as e:
                logger.error(f"Error processing event {event}: {e}")

    def _handle_llm_start(self, event: dict):
        """Handle LLM call start event."""
        run_id = event.get("run_id")

        # Check if there's already an active run
        active_run = mlflow.active_run()

        if not run_id and not active_run:
            # Start a new run only if none exists
            try:
                run = mlflow.start_run(run_name=event.get("name", "llm_call"))
                event["run_id"] = run.info.run_id
            except Exception as e:
                logger.warning(f"Could not start new MLflow run: {e}")
                return
        elif active_run:
            # Use the existing active run
            event["run_id"] = active_run.info.run_id

        # Log parameters
        try:
            mlflow.log_param("model", event.get("model", "unknown"))
            mlflow.log_param("provider", event.get("provider", "unknown"))

            if "params" in event:
                for key, value in event["params"].items():
                    if isinstance(value, (str, int, float, bool)):
                        mlflow.log_param(f"llm_{key}", value)
        except Exception as e:
            logger.warning(f"Could not log parameters: {e}")

    def _handle_llm_end(self, event: dict):
        """Handle LLM call end event."""
        usage = event.get("usage", {})
        model = event.get("model", "unknown")

        # Track costs
        if usage:
            try:
                cost_entry = self.cost_tracker.track_cost(
                    model_name=model,
                    input_tokens=usage.get("prompt_tokens", 0),
                    output_tokens=usage.get("completion_tokens", 0),
                    run_id=event.get("run_id"),
                    metadata=event.get("metadata", {}),
                    log_to_mlflow=True,
                )
            except Exception as e:
                logger.warning(f"Could not track cost: {e}")

        # Log metrics
        metrics = {
            "llm_duration_ms": event.get("duration_ms", 0),
            "llm_success": 1 if not event.get("error") else 0,
        }

        if usage:
            metrics.update(
                {
                    "llm_prompt_tokens": usage.get("prompt_tokens", 0),
                    "llm_completion_tokens": usage.get("completion_tokens", 0),
                    "llm_total_tokens": usage.get("total_tokens", 0),
                }
            )

        try:
            mlflow.log_metrics(metrics)
        except Exception as e:
            logger.warning(f"Could not log metrics: {e}")

        # Only end run if we were explicitly told to
        if event.get("end_run"):
            try:
                mlflow.end_run()
            except Exception as e:
                logger.warning(f"Could not end run: {e}")

    def _handle_component_start(self, event: dict):
        """Handle component start event."""
        try:
            mlflow.start_run(
                run_name=event.get("name", "component"),
                nested=True,
                tags={
                    "component_type": event.get("component_type", "unknown"),
                    "component_id": event.get("component_id", str(uuid.uuid4())),
                },
            )
        except Exception as e:
            logger.warning(f"Could not start component run: {e}")

    def _handle_component_end(self, event: dict):
        """Handle component end event."""
        try:
            if event.get("outputs"):
                mlflow.log_text(
                    json.dumps(event["outputs"], default=str), "outputs.json"
                )

            mlflow.log_metric("component_duration_ms", event.get("duration_ms", 0))
            mlflow.log_metric("component_success", 1 if not event.get("error") else 0)

            mlflow.end_run()
        except Exception as e:
            logger.warning(f"Could not handle component end: {e}")

    def _handle_metric(self, event: dict):
        """Handle metric logging event."""
        metrics = event.get("metrics", {})
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(key, value)

    async def track_llm_start(self, **kwargs):
        """Track LLM call start without blocking."""
        event = {
            "type": "llm_start",
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }

        try:
            self.event_queue.put_nowait(event)
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping LLM start event")

    async def track_llm_end(self, **kwargs):
        """Track LLM call end without blocking."""
        event = {
            "type": "llm_end",
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }

        try:
            self.event_queue.put_nowait(event)
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping LLM end event")

    async def track_component_start(self, **kwargs):
        """Track component start without blocking."""
        event = {
            "type": "component_start",
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }

        try:
            self.event_queue.put_nowait(event)
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping component start event")

    async def track_component_end(self, **kwargs):
        """Track component end without blocking."""
        event = {
            "type": "component_end",
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }

        try:
            self.event_queue.put_nowait(event)
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping component end event")

    def track_sync(self, event: dict):
        """Track event from sync code without blocking."""
        try:
            self.sync_queue.put_nowait(event)
        except:
            logger.warning("Sync queue full, dropping event")

    def cleanup(self):
        """Cleanup resources."""
        self.running = False

        # Process remaining events
        remaining_events = []

        # Drain async queue
        while not self.event_queue.empty():
            try:
                remaining_events.append(self.event_queue.get_nowait())
            except:
                break

        # Drain sync queue
        while not self.sync_queue.empty():
            try:
                remaining_events.append(self.sync_queue.get_nowait())
            except:
                break

        # Process remaining events
        if remaining_events:
            self._process_events(remaining_events)

        # Shutdown executor
        self.executor.shutdown(wait=True)

        # Log final cost summary
        try:
            self.cost_tracker.log_cost_summary_to_mlflow()
        except:
            pass


# Global monitor instance
_monitor = AsyncMonitor()


async def initialize_async(
    cost_rates: Optional[dict] = None, experiment_name: Optional[str] = None, **kwargs
):
    """Initialize async monitoring."""
    await _monitor.initialize(experiment_name)
    if cost_rates:
        _monitor.cost_tracker.cost_rates.update(cost_rates)
