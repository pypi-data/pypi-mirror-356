"""
Microservmon - Lightweight logging collector for microservice requests and functions and API endpoints
"""
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from contextlib import contextmanager
from collections import defaultdict
from ipulse_shared_base_ftredge import (LogLevel, AbstractResource,
                                      ProgressStatus, Action,
                                      Alert, StructLog)
from ipulse_shared_base_ftredge.status import StatusCounts, map_progress_status_to_log_level, eval_statuses

class Microservmon:
    """
    Microservmon is a lightweight version of Pipelinemon designed specifically for monitoring
    microservice events such as HTTP Requests, PubSub Triggers etc within execution environment like
    Cloud Functions, Cloud Run etc.

    It provides:
    1. Structured logging with context tracking
    2. Performance metrics capture per trace
    3. Microservice health monitoring
    4. Integration with FastAPI request/response cycle
    5. Memory-efficient trace lifecycle management
    """

    def __init__(self, logger,
                 base_context: str,
                 microservice_name: str,
                 max_log_field_len: Optional[int] = 8000,
                 max_log_dict_byte_size: Optional[float] = 256 * 1024 * 0.80,
                 exclude_none_from_logs: bool = True):
        """
        Initialize Microservmon with basic configuration.

        Args:
            logger: The logger instance to use for logging
            base_context: Base context information for all logs
            microservice_name: Name of the microservice being monitored
            max_log_field_len: Maximum length for any string field in logs
            max_log_dict_byte_size: Maximum byte size for log dictionary
            exclude_none_from_logs: Whether to exclude None values from log output (default: True)
        """
        # Set up microservice tracking details
        self._microservice_name = microservice_name
        self._microservice_start_time = time.time()

        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        uuid_suffix = str(uuid.uuid4())[:8]  # Take first 8 chars of UUID
        self._id = f"{timestamp}_{uuid_suffix}"

        # Set up context handling
        self._base_context = base_context
        self._context_stack = []

        # Configure logging
        self._logger = logger
        self._max_log_field_len = max_log_field_len
        self._max_log_dict_byte_size = max_log_dict_byte_size
        self._exclude_none_from_logs = exclude_none_from_logs

        # Trace-based tracking - key change from original
        self._active_traces: Dict[str, Dict[str, Any]] = {}

        # Microservice-wide metrics (aggregated across all traces)
        self._microservice_metrics = {
            "total_traces": 0,
            "active_traces": 0,
            "completed_traces": 0,
            "failed_traces": 0,
            "by_event_count": defaultdict(int),
            "by_level_code_count": defaultdict(int),
            "status_counts": StatusCounts()  # Add StatusCounts for better status tracking
        }

        # Log microservice startup
        self._log_microservice_start()

    def _log_microservice_start(self):
        """Log the microservice instance startup."""
        startup_log = StructLog(
            level=LogLevel.INFO,
            resource=AbstractResource.MICROSERVMON,
            action=Action.EXECUTE,
            progress_status=ProgressStatus.STARTED,
            description=f"Microservice {self.microservice_name} instance started",
            collector_id=self.id,
            base_context=self.base_context,
            context="microservice_startup"
        )
        self._write_log_to_logger(startup_log)

    @property
    def id(self) -> str:
        """Get the unique ID for this microservice instance."""
        return self._id

    @property
    def base_context(self) -> str:
        """Get the base context for this microservice execution."""
        return self._base_context

    @property
    def microservice_name(self) -> str:
        """Get the microservice name being monitored."""
        return self._microservice_name

    @property
    def microservice_metrics(self) -> Dict[str, Any]:
        """Get the current microservice-wide metrics."""
        metrics = self._microservice_metrics.copy()
        metrics["by_event_count"] = dict(metrics["by_event_count"])
        metrics["by_level_code_count"] = dict(metrics["by_level_code_count"])
        return metrics

    @property
    def active_trace_count(self) -> int:
        """Get count of currently active traces."""
        return len(self._active_traces)

    @property
    def current_context(self) -> str:
        """Get the current context stack as a string."""
        return " >> ".join(self._context_stack) if self._context_stack else "root"

    @contextmanager
    def context(self, context_name: str):
        """
        Context manager for tracking execution context.
        Note: This is for microservice-wide context, not trace-specific.

        Args:
            context_name: The name of the current execution context
        """
        self.push_context(context_name)
        try:
            yield
        finally:
            self.pop_context()

    def push_context(self, context: str):
        """Add a context level to the stack."""
        self._context_stack.append(context)

    def pop_context(self):
        """Remove the most recent context from the stack."""
        if self._context_stack:
            return self._context_stack.pop()

    def start_trace(self, description: Optional[str] = None) -> str:
        """
        Start monitoring a new trace (request/event) with auto-generated trace ID.

        Args:
            description: Optional description of the trace

        Returns:
            str: Auto-generated trace_id
        """
        # Auto-generate trace ID
        timestamp = datetime.now(timezone.utc).strftime('%H%M%S_%f')[:-3]  # Include milliseconds
        trace_id = f"trace_{timestamp}_{str(uuid.uuid4())[:6]}"

        start_time = time.time()

        # Initialize trace metrics with StatusCounts
        self._active_traces[trace_id] = {
            "start_time": start_time,
            "status": ProgressStatus.IN_PROGRESS.name,
            "by_event_count": defaultdict(int),
            "by_level_code_count": defaultdict(int),
            "status_counts": StatusCounts()  # Track status progression within trace
        }

        # Add initial status to trace
        self._active_traces[trace_id]["status_counts"].add_status(ProgressStatus.IN_PROGRESS)

        # Update microservice metrics
        self._microservice_metrics["total_traces"] += 1
        self._microservice_metrics["active_traces"] = len(self._active_traces)
        self._microservice_metrics["status_counts"].add_status(ProgressStatus.IN_PROGRESS)

        # Log the trace start using StructLog
        msg = description if description else f"Starting trace {trace_id}"
        start_log = StructLog(
            level=LogLevel.INFO,
            description=msg,
            resource=AbstractResource.MICROSERVICE_TRACE,
            action=Action.EXECUTE,
            progress_status=ProgressStatus.IN_PROGRESS
        )
        self.log(start_log, trace_id)

        return trace_id

    def end_trace(self, trace_id: str, force_status: Optional[ProgressStatus] = None) -> None:
        """
        End monitoring for a trace and record final metrics.
        Status is automatically calculated based on trace metrics unless forced.

        Args:
            trace_id: The trace identifier to end
            force_status: Optional status to force, overriding automatic calculation
        """
        if trace_id not in self._active_traces:
            # Log warning about unknown trace using StructLog
            warning_log = StructLog(
                level=LogLevel.WARNING,
                description=f"Attempted to end unknown trace: {trace_id}",
                resource=AbstractResource.MICROSERVICE_TRACE,
                action=Action.EXECUTE,
                progress_status=ProgressStatus.UNFINISHED,
                alert=Alert.NOT_FOUND
            )
            self.log(warning_log)
            return

        trace_metrics = self._active_traces[trace_id]

        # Calculate duration
        end_time = time.time()
        duration_ms = int((end_time - trace_metrics["start_time"]) * 1000)
        trace_metrics["duration_ms"] = duration_ms
        trace_metrics["end_time"] = end_time

        # Get readable error/warning counts using existing helper functions
        error_count = self._get_error_count_for_trace(trace_id)
        warning_count = self._get_warning_count_for_trace(trace_id)

        # Use status helpers for intelligent status calculation
        if force_status is not None:
            final_status = force_status
            level = map_progress_status_to_log_level(final_status)
        else:
            # Build status list based on log levels for evaluation
            status_list = []
            if error_count > 0:
                status_list.append(ProgressStatus.FINISHED_WITH_ISSUES)
            elif warning_count > 0:
                status_list.append(ProgressStatus.DONE_WITH_WARNINGS)
            else:
                status_list.append(ProgressStatus.DONE)

            # Use eval_statuses for consistent status evaluation
            final_status = eval_statuses(
                status_list,
                fail_or_unfinish_if_any_pending=True,  # Since this is end of trace
                issues_allowed=True
            )
            level = map_progress_status_to_log_level(final_status)

        # Update trace status
        trace_metrics["status"] = final_status.name
        trace_metrics["status_counts"].add_status(final_status)

        # Prepare summary message
        status_source = "FORCED" if force_status is not None else "AUTO"
        summary_msg = (
            f"Trace {trace_id} completed with status {final_status.name} ({status_source}). "
            f"Duration: {duration_ms}ms. "
            f"Errors: {error_count}, Warnings: {warning_count}"
        )

        # Log the completion using StructLog
        completion_log = StructLog(
            level=level,
            description=summary_msg,
            resource=AbstractResource.MICROSERVMON,
            action=Action.EXECUTE,
            progress_status=final_status
        )
        self.log(completion_log, trace_id)

        # Update microservice-wide metrics using StatusCounts
        self._microservice_metrics["completed_traces"] += 1
        if final_status in ProgressStatus.failure_statuses():
            self._microservice_metrics["failed_traces"] += 1

        # Add final status to microservice status counts
        self._microservice_metrics["status_counts"].add_status(final_status)

        # Aggregate trace metrics to microservice level
        for event, count in trace_metrics["by_event_count"].items():
            self._microservice_metrics["by_event_count"][event] += count
        for level_code, count in trace_metrics["by_level_code_count"].items():
            self._microservice_metrics["by_level_code_count"][level_code] += count

        # Clean up trace data from memory
        del self._active_traces[trace_id]
        self._microservice_metrics["active_traces"] = len(self._active_traces)

    def log(self, log: StructLog, trace_id: Optional[str] = None) -> None:
        """
        Log a StructLog message with trace context.

        Args:
            log: StructLog instance to log
            trace_id: Optional trace ID for trace-specific logging
        """
        # Calculate elapsed time
        elapsed_ms = None
        if trace_id and trace_id in self._active_traces:
            start_time = self._active_traces[trace_id]["start_time"]
            elapsed_ms = int((time.time() - start_time) * 1000)
        else:
            # Use microservice start time if no trace
            elapsed_ms = int((time.time() - self._microservice_start_time) * 1000)

        # Set microservice-specific context on the log
        log.collector_id = self.id
        log.base_context = self.base_context
        # Context includes trace_id automatically via StructLog
        log.context = f"{self.current_context} >> {trace_id}" if trace_id else self.current_context
        log.trace_id = trace_id

        # Append elapsed time to existing notes
        existing_note = log.note or ""
        elapsed_note = f"elapsed_ms: {elapsed_ms}"
        log.note = f"{existing_note}; {elapsed_note}" if existing_note else elapsed_note

        # Update metrics for the trace or microservice
        self._update_counts(log, trace_id)

        # Write to logger
        self._write_log_to_logger(log)

    def _update_counts(self, log: StructLog, trace_id: Optional[str] = None):
        """Update counts for event tracking."""
        event_tuple = log.getEvent()
        level = log.level

        # Update trace-specific metrics if trace_id provided
        if trace_id and trace_id in self._active_traces:
            trace_metrics = self._active_traces[trace_id]
            trace_metrics["by_event_count"][event_tuple] += 1
            trace_metrics["by_level_code_count"][level.value] += 1

    def _get_error_count_for_trace(self, trace_id: str) -> int:
        """Get total error count (ERROR + CRITICAL) for a specific trace."""
        if trace_id not in self._active_traces:
            return 0

        trace_metrics = self._active_traces[trace_id]
        return (trace_metrics["by_level_code_count"].get(LogLevel.ERROR.value, 0) +
                trace_metrics["by_level_code_count"].get(LogLevel.CRITICAL.value, 0))

    def _get_warning_count_for_trace(self, trace_id: str) -> int:
        """Get warning count for a specific trace."""
        if trace_id not in self._active_traces:
            return 0

        trace_metrics = self._active_traces[trace_id]
        return trace_metrics["by_level_code_count"].get(LogLevel.WARNING.value, 0)

    def get_readable_level_counts_for_trace(self, trace_id: str) -> Dict[str, int]:
        """Get readable level counts for a specific trace."""
        if trace_id not in self._active_traces:
            return {}

        trace_metrics = self._active_traces[trace_id]
        readable_counts = {}

        for level_code, count in trace_metrics["by_level_code_count"].items():
            if count > 0:
                # Convert level code back to LogLevel enum and get name
                for level in LogLevel:
                    if level.value == level_code:
                        readable_counts[level.name] = count
                        break

        return readable_counts

    def get_readable_microservice_level_counts(self) -> Dict[str, int]:
        """Get readable level counts for the entire microservice."""
        readable_counts = {}

        for level_code, count in self._microservice_metrics["by_level_code_count"].items():
            if count > 0:
                # Convert level code back to LogLevel enum and get name
                for level in LogLevel:
                    if level.value == level_code:
                        readable_counts[level.name] = count
                        break

        return readable_counts

    def get_microservice_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary using StatusCounts"""
        status_counts = self._microservice_metrics["status_counts"]

        return {
            "microservice_name": self.microservice_name,
            "microservice_id": self.id,
            "active_traces": self.active_trace_count,
            "total_traces": self._microservice_metrics["total_traces"],
            "completed_traces": self._microservice_metrics["completed_traces"],
            "failed_traces": self._microservice_metrics["failed_traces"],
            "status_breakdown": status_counts.get_count_breakdown(),
            "completion_rate": status_counts.completion_rate,
            "success_rate": status_counts.success_rate,
            "has_issues": status_counts.has_issues,
            "has_failures": status_counts.has_failures,
            "readable_level_counts": self.get_readable_microservice_level_counts()
        }

    def evaluate_microservice_health(self) -> Dict[str, Any]:
        """Evaluate overall microservice health using status helpers"""
        status_counts = self._microservice_metrics["status_counts"]

        # Determine overall health status
        if status_counts.has_failures:
            health_status = "UNHEALTHY"
            health_level = LogLevel.ERROR
        elif status_counts.has_issues:
            health_status = "DEGRADED"
            health_level = LogLevel.WARNING
        elif status_counts.has_warnings:
            health_status = "WARNING"
            health_level = LogLevel.WARNING
        else:
            health_status = "HEALTHY"
            health_level = LogLevel.INFO

        return {
            "health_status": health_status,
            "health_level": health_level.name,
            "summary": status_counts.get_summary(),
            "metrics": self.get_microservice_status_summary()
        }

    def log_health_check(self) -> None:
        """Log a health check using the status evaluation"""
        health = self.evaluate_microservice_health()

        health_log = StructLog(
            level=LogLevel[health["health_level"]],
            description=f"Microservice health check: {health['health_status']}",
            resource=AbstractResource.MICROSERVMON,
            action=Action.VALIDATE,
            progress_status=ProgressStatus.DONE,
            note=health["summary"]
        )
        self.log(health_log)

    # Legacy compatibility methods
    def start(self, description: Optional[str] = None) -> None:
        """Legacy method for backward compatibility."""
        trace_id = self.start_trace(description)

    def end(self, force_status: Optional[ProgressStatus] = None) -> Dict[str, Any]:
        """Legacy method for backward compatibility."""
        # Find the most recent trace or create a dummy one
        if self._active_traces:
            trace_id = max(self._active_traces.keys())
            self.end_trace(trace_id, force_status)
            # Return microservice metrics for legacy compatibility
            return self.microservice_metrics
        return {}

    @property
    def metrics(self) -> Dict[str, Any]:
        """Legacy property for backward compatibility."""
        return self.microservice_metrics

    def _write_log_to_logger(self, log: StructLog):
        """Write structured log to the logger."""
        log_dict = log.to_dict(
            max_field_len=self._max_log_field_len,
            byte_size_limit=self._max_log_dict_byte_size,
            exclude_none=self._exclude_none_from_logs
        )

        # Write to logger based on level
        if log.level.value >= LogLevel.ERROR.value:
            self._logger.error(log_dict)
        elif log.level.value >= LogLevel.WARNING.value:
            self._logger.warning(log_dict)
        elif log.level.value >= LogLevel.INFO.value:
            self._logger.info(log_dict)
        else:
            self._logger.debug(log_dict)