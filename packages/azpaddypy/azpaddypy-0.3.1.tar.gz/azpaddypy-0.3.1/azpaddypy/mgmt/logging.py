import logging
import os
import functools
import time
import asyncio
from typing import Optional, Dict, Any, Union, Callable
from datetime import datetime
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode, Span
from opentelemetry import baggage
from opentelemetry.context import Context


class AzureLogger:
    """Azure-integrated logger with OpenTelemetry distributed tracing.

    Provides comprehensive logging with Azure Monitor integration, correlation
    tracking, baggage propagation, and automated function tracing for Azure
    applications with seamless local development support.

    Supports all standard logging levels (debug, info, warning, error, exception, 
    critical) with enhanced context including trace IDs, correlation IDs, and 
    baggage propagation.

    Attributes:
        service_name: Service identifier for telemetry
        service_version: Service version for context
        connection_string: Application Insights connection string
        logger: Python logger instance
        tracer: OpenTelemetry tracer for spans
    """

    def __init__(
        self,
        service_name: str,
        service_version: str = "1.0.0",
        connection_string: Optional[str] = None,
        log_level: int = logging.INFO,
        enable_console_logging: bool = True,
        custom_resource_attributes: Optional[Dict[str, str]] = None,
        instrumentation_options: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Azure Logger with OpenTelemetry tracing.

        Args:
            service_name: Service identifier for telemetry
            service_version: Service version for metadata
            connection_string: Application Insights connection string
            log_level: Python logging level (default: INFO)
            enable_console_logging: Enable console output for local development
            custom_resource_attributes: Additional OpenTelemetry resource attributes
            instrumentation_options: Azure Monitor instrumentation options
        """
        self.service_name = service_name
        self.service_version = service_version
        self.connection_string = connection_string or os.getenv(
            "APPLICATIONINSIGHTS_CONNECTION_STRING"
        )

        # Configure resource attributes
        resource_attributes = {
            "service.name": service_name,
            "service.version": service_version,
            "service.instance.id": os.getenv("WEBSITE_INSTANCE_ID", "local"),
        }

        if custom_resource_attributes:
            resource_attributes.update(custom_resource_attributes)

        # Configure Azure Monitor if connection string available
        if self.connection_string:
            try:
                configure_azure_monitor(
                    connection_string=self.connection_string,
                    resource_attributes=resource_attributes,
                    enable_live_metrics=True,
                    instrumentation_options=instrumentation_options,
                )
                self._telemetry_enabled = True
            except Exception as e:
                print(f"Warning: Failed to configure Azure Monitor: {e}")
                self._telemetry_enabled = False
        else:
            self._telemetry_enabled = False
            print(
                "Warning: No Application Insights connection string found. Telemetry disabled."
            )

        # Configure Python logger
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(log_level)
        self.logger.handlers.clear()

        if enable_console_logging:
            self._setup_console_handler()

        # Initialize OpenTelemetry tracer and correlation context
        self.tracer = trace.get_tracer(__name__)
        self._correlation_id = None

        self.info(
            f"Azure Logger initialized for service '{service_name}' v{service_version}"
        )

    def _setup_console_handler(self):
        """Configure console handler for local development."""
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def set_correlation_id(self, correlation_id: str):
        """Set correlation ID for request/transaction tracking.

        Args:
            correlation_id: Unique identifier for transaction correlation
        """
        self._correlation_id = correlation_id

    def get_correlation_id(self) -> Optional[str]:
        """Get current correlation ID.

        Returns:
            Current correlation ID if set, otherwise None
        """
        return self._correlation_id

    def set_baggage(self, key: str, value: str) -> Context:
        """Set baggage item in OpenTelemetry context.

        Args:
            key: Baggage key
            value: Baggage value

        Returns:
            Updated context with baggage item
        """
        return baggage.set_baggage(key, value)

    def get_baggage(self, key: str) -> Optional[str]:
        """Get baggage item from current context.

        Args:
            key: Baggage key

        Returns:
            Baggage value if exists, otherwise None
        """
        return baggage.get_baggage(key)

    def get_all_baggage(self) -> Dict[str, str]:
        """Get all baggage items from current context.

        Returns:
            Dictionary of all baggage items
        """
        return dict(baggage.get_all())

    def _enhance_extra(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enrich log records with contextual information.

        Args:
            extra: Optional custom data dictionary

        Returns:
            Enhanced dictionary with service context, correlation ID, trace
            context, and baggage items
        """
        enhanced_extra = {
            "service_name": self.service_name,
            "service_version": self.service_version,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if self._correlation_id:
            enhanced_extra["correlation_id"] = self._correlation_id

        # Add span context if available
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            enhanced_extra["trace_id"] = format(span_context.trace_id, "032x")
            enhanced_extra["span_id"] = format(span_context.span_id, "016x")

        # Add baggage items
        baggage_items = self.get_all_baggage()
        if baggage_items:
            enhanced_extra["baggage"] = baggage_items

        if isinstance(extra, dict):
            enhanced_extra.update(extra)

        return enhanced_extra

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log debug message with enhanced context."""
        self.logger.debug(message, extra=self._enhance_extra(extra))

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log info message with enhanced context."""
        self.logger.info(message, extra=self._enhance_extra(extra))

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message with enhanced context."""
        self.logger.warning(message, extra=self._enhance_extra(extra))

    def error(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        exc_info: bool = True,
    ):
        """Log error message with enhanced context and exception info."""
        self.logger.error(message, extra=self._enhance_extra(extra), exc_info=exc_info)

    def exception(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log exception message with enhanced context and automatic exception info.
        
        This method is a convenience method equivalent to calling error() with 
        exc_info=True. It should typically be called only from exception handlers.
        
        Args:
            message: Exception message to log
            extra: Additional custom properties
        """
        self.logger.error(message, extra=self._enhance_extra(extra), exc_info=True)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log critical message with enhanced context."""
        self.logger.critical(message, extra=self._enhance_extra(extra))

    def log_function_execution(
        self,
        function_name: str,
        duration_ms: float,
        success: bool = True,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Log function execution metrics for performance monitoring.

        Args:
            function_name: Name of executed function
            duration_ms: Execution duration in milliseconds
            success: Whether function executed successfully
            extra: Additional custom properties
        """
        log_data = {
            "function_name": function_name,
            "duration_ms": duration_ms,
            "success": success,
            "performance_category": "function_execution",
        }

        if extra:
            log_data.update(extra)

        message = f"Function '{function_name}' executed in {duration_ms:.2f}ms - {'SUCCESS' if success else 'FAILED'}"

        if success:
            self.info(message, extra=log_data)
        else:
            self.error(message, extra=log_data, exc_info=False)

    def log_request(
        self,
        method: str,
        url: str,
        status_code: int,
        duration_ms: float,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Log HTTP request with comprehensive details.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            status_code: HTTP response status code
            duration_ms: Request duration in milliseconds
            extra: Additional custom properties
        """
        log_data = {
            "http_method": method,
            "http_url": str(url),
            "http_status_code": status_code,
            "duration_ms": duration_ms,
            "request_category": "http_request",
        }

        if extra:
            log_data.update(extra)

        # Determine log level and status based on status code
        if status_code < 400:
            log_level = logging.INFO
            status_text = "SUCCESS"
        elif status_code < 500:
            log_level = logging.WARNING
            status_text = "CLIENT_ERROR"
        else:
            log_level = logging.ERROR
            status_text = "SERVER_ERROR"

        message = (
            f"{method} {url} - {status_code} - {duration_ms:.2f}ms - {status_text}"
        )
        self.logger.log(log_level, message, extra=self._enhance_extra(log_data))

    def create_span(
        self,
        span_name: str,
        attributes: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ) -> Span:
        """Create OpenTelemetry span for distributed tracing.

        Args:
            span_name: Name for the span
            attributes: Initial span attributes

        Returns:
            OpenTelemetry span context manager
        """
        span = self.tracer.start_span(span_name)

        # Add default service attributes
        span.set_attribute("service.name", self.service_name)
        span.set_attribute("service.version", self.service_version)

        if self._correlation_id:
            span.set_attribute("correlation.id", self._correlation_id)

        # Add custom attributes
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, value)

        return span

    def _setup_span_for_function_trace(
        self,
        span: Span,
        func: Callable,
        is_async: bool,
        log_args: bool,
        args: tuple,
        kwargs: dict,
        log_result: bool,
        log_execution: bool,
    ):
        """Configure span attributes for function tracing."""
        span.set_attribute("function.name", func.__name__)
        span.set_attribute("function.module", func.__module__)
        span.set_attribute("service.name", self.service_name)
        span.set_attribute("function.is_async", is_async)

        # Add decorator parameters as span attributes
        span.set_attribute("function.decorator.log_args", log_args)
        span.set_attribute("function.decorator.log_result", log_result)
        span.set_attribute("function.decorator.log_execution", log_execution)

        if self._correlation_id:
            span.set_attribute("correlation.id", self._correlation_id)

        if log_args:
            if args:
                span.set_attribute("function.args_count", len(args))
                # Add positional arguments as span attributes
                import inspect
                try:
                    sig = inspect.signature(func)
                    param_names = list(sig.parameters.keys())
                    for i, arg_value in enumerate(args):
                        param_name = param_names[i] if i < len(param_names) else f"arg_{i}"
                        try:
                            # Convert to string for safe serialization
                            attr_value = str(arg_value)
                            # Truncate if too long to avoid excessive data
                            if len(attr_value) > 1000:
                                attr_value = attr_value[:1000] + "..."
                            span.set_attribute(f"function.arg.{param_name}", attr_value)
                        except Exception:
                            span.set_attribute(f"function.arg.{param_name}", "<non-serializable>")
                except Exception:
                    # Fallback if signature inspection fails
                    for i, arg_value in enumerate(args):
                        try:
                            attr_value = str(arg_value)
                            if len(attr_value) > 1000:
                                attr_value = attr_value[:1000] + "..."
                            span.set_attribute(f"function.arg.{i}", attr_value)
                        except Exception:
                            span.set_attribute(f"function.arg.{i}", "<non-serializable>")
                            
            if kwargs:
                span.set_attribute("function.kwargs_count", len(kwargs))
                # Add keyword arguments as span attributes
                for key, value in kwargs.items():
                    try:
                        attr_value = str(value)
                        # Truncate if too long to avoid excessive data
                        if len(attr_value) > 1000:
                            attr_value = attr_value[:1000] + "..."
                        span.set_attribute(f"function.kwarg.{key}", attr_value)
                    except Exception:
                        span.set_attribute(f"function.kwarg.{key}", "<non-serializable>")

    def _handle_function_success(
        self,
        span: Span,
        func: Callable,
        duration_ms: float,
        result: Any,
        log_result: bool,
        log_execution: bool,
        is_async: bool,
        args: tuple,
        kwargs: dict,
    ):
        """Handle successful function execution in tracing."""
        span.set_attribute("function.duration_ms", duration_ms)
        span.set_attribute("function.success", True)
        span.set_status(Status(StatusCode.OK))

        if log_result and result is not None:
            span.set_attribute("function.has_result", True)
            span.set_attribute("function.result_type", type(result).__name__)

        if log_execution:
            self.log_function_execution(
                func.__name__,
                duration_ms,
                True,
                {
                    "args_count": len(args) if args else 0,
                    "kwargs_count": len(kwargs) if kwargs else 0,
                    "is_async": is_async,
                },
            )

        log_prefix = "Async function" if is_async else "Function"
        self.debug(f"{log_prefix} execution completed: {func.__name__}")

    def _handle_function_exception(
        self,
        span: Span,
        func: Callable,
        duration_ms: float,
        e: Exception,
        log_execution: bool,
        is_async: bool,
    ):
        """Handle failed function execution in tracing."""
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.record_exception(e)
        span.set_attribute("function.duration_ms", duration_ms)
        span.set_attribute("function.success", False)
        span.set_attribute("error.type", type(e).__name__)
        span.set_attribute("error.message", str(e))

        if log_execution:
            self.log_function_execution(
                func.__name__,
                duration_ms,
                False,
                {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "is_async": is_async,
                },
            )

        log_prefix = "Async function" if is_async else "Function"
        self.error(f"{log_prefix} execution failed: {func.__name__} - {str(e)}")

    def trace_function(
        self,
        function_name: Optional[str] = None,
        log_execution: bool = True,
        log_args: bool = True,
        log_result: bool = False
    ) -> Callable:
        """Decorator for automatic function execution tracing.

        Supports both synchronous and asynchronous functions with comprehensive
        logging and OpenTelemetry span creation.

        Args:
            function_name: Custom span name (defaults to function name)
            log_execution: Whether to log execution metrics
            log_args: Whether to log function arguments
            log_result: Whether to log function result
        """

        def decorator(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                span_name = function_name or f"{func.__module__}.{func.__name__}"
                with self.tracer.start_as_current_span(span_name) as span:
                    self._setup_span_for_function_trace(
                        span, func, True, log_args, args, kwargs, log_result, log_execution
                    )
                    start_time = time.time()
                    try:
                        self.debug(
                            f"Starting async function execution: {func.__name__}"
                        )
                        result = await func(*args, **kwargs)
                        duration_ms = (time.time() - start_time) * 1000
                        self._handle_function_success(
                            span,
                            func,
                            duration_ms,
                            result,
                            log_result,
                            log_execution,
                            True,
                            args,
                            kwargs,
                        )
                        return result
                    except Exception as e:
                        duration_ms = (time.time() - start_time) * 1000
                        self._handle_function_exception(
                            span, func, duration_ms, e, log_execution, True
                        )
                        raise

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                span_name = function_name or f"{func.__module__}.{func.__name__}"
                with self.tracer.start_as_current_span(span_name) as span:
                    self._setup_span_for_function_trace(
                        span, func, False, log_args, args, kwargs, log_result, log_execution
                    )
                    start_time = time.time()
                    try:
                        self.debug(f"Starting function execution: {func.__name__}")
                        result = func(*args, **kwargs)
                        duration_ms = (time.time() - start_time) * 1000
                        self._handle_function_success(
                            span,
                            func,
                            duration_ms,
                            result,
                            log_result,
                            log_execution,
                            False,
                            args,
                            kwargs,
                        )
                        return result
                    except Exception as e:
                        duration_ms = (time.time() - start_time) * 1000
                        self._handle_function_exception(
                            span, func, duration_ms, e, log_execution, False
                        )
                        raise

            # Return appropriate wrapper based on function type
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper

        return decorator

    def add_span_attributes(self, attributes: Dict[str, Union[str, int, float, bool]]):
        """Add attributes to current active span."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            for key, value in attributes.items():
                current_span.set_attribute(key, value)

    def add_span_event(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Add event to current active span."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            event_attributes = attributes or {}
            if self._correlation_id:
                event_attributes["correlation_id"] = self._correlation_id
            current_span.add_event(name, event_attributes)

    def set_span_status(
        self, status_code: StatusCode, description: Optional[str] = None
    ):
        """Set status of current active span."""
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            current_span.set_status(Status(status_code, description))

    def log_with_span(
        self,
        span_name: str,
        message: str,
        level: int = logging.INFO,
        extra: Optional[Dict[str, Any]] = None,
        span_attributes: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ):
        """Log message within a span context.

        Args:
            span_name: Name for the span
            message: Log message
            level: Python logging level
            extra: Additional log properties
            span_attributes: Attributes to add to span
        """
        with self.tracer.start_as_current_span(span_name) as span:
            if span_attributes:
                for key, value in span_attributes.items():
                    span.set_attribute(key, value)

            self.logger.log(level, message, extra=self._enhance_extra(extra))

    def log_dependency(
        self,
        dependency_type: str,
        name: str,
        command: str,
        success: bool,
        duration_ms: float,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Log external dependency calls for monitoring.

        Args:
            dependency_type: Type of dependency (SQL, HTTP, etc.)
            name: Dependency identifier
            command: Command/query executed
            success: Whether call was successful
            duration_ms: Call duration in milliseconds
            extra: Additional properties
        """
        log_data = {
            "dependency_type": dependency_type,
            "dependency_name": name,
            "dependency_command": command,
            "dependency_success": success,
            "duration_ms": duration_ms,
            "category": "dependency_call",
        }

        if extra:
            log_data.update(extra)

        log_level = logging.INFO if success else logging.ERROR
        status = "SUCCESS" if success else "FAILED"
        message = f"Dependency call: {dependency_type}:{name} - {duration_ms:.2f}ms - {status}"

        self.logger.log(log_level, message, extra=self._enhance_extra(log_data))

    def flush(self):
        """Flush pending telemetry data."""
        if self._telemetry_enabled:
            try:
                from opentelemetry.sdk.trace import TracerProvider

                tracer_provider = trace.get_tracer_provider()
                if hasattr(tracer_provider, "force_flush"):
                    tracer_provider.force_flush(timeout_millis=5000)
            except Exception as e:
                self.warning(f"Failed to flush telemetry: {e}")


# Factory functions with logger caching
_loggers: Dict[Any, "AzureLogger"] = {}


def create_app_logger(
    service_name: str,
    service_version: str = "1.0.0",
    connection_string: Optional[str] = None,
    log_level: int = logging.INFO,
    enable_console_logging: bool = True,
    custom_resource_attributes: Optional[Dict[str, str]] = None,
    instrumentation_options: Optional[Dict[str, Any]] = None,
) -> AzureLogger:
    """Create cached AzureLogger instance for applications.

    Returns existing logger if one with same configuration exists.

    Args:
        service_name: Service identifier for telemetry
        service_version: Service version for metadata
        connection_string: Application Insights connection string
        log_level: Python logging level
        enable_console_logging: Enable console output
        custom_resource_attributes: Additional OpenTelemetry resource attributes
        instrumentation_options: Azure Monitor instrumentation options

    Returns:
        Configured AzureLogger instance
    """
    resolved_connection_string = connection_string or os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )

    attr_items = (
        tuple(sorted(custom_resource_attributes.items()))
        if custom_resource_attributes
        else None
    )

    params_key = (
        service_name,
        service_version,
        resolved_connection_string,
        log_level,
        enable_console_logging,
        attr_items,
    )

    if params_key in _loggers:
        return _loggers[params_key]

    logger = AzureLogger(
        service_name=service_name,
        service_version=service_version,
        connection_string=connection_string,
        log_level=log_level,
        enable_console_logging=enable_console_logging,
        custom_resource_attributes=custom_resource_attributes,
    )
    _loggers[params_key] = logger
    return logger


def create_function_logger(
    function_app_name: str,
    function_name: str,
    service_version: str = "1.0.0",
    connection_string: Optional[str] = None,
    instrumentation_options: Optional[Dict[str, Any]] = None,
) -> AzureLogger:
    """Create AzureLogger optimized for Azure Functions.

    Args:
        function_app_name: Azure Function App name
        function_name: Specific function name
        service_version: Service version for metadata
        connection_string: Application Insights connection string
        instrumentation_options: Azure Monitor instrumentation options

    Returns:
        Configured AzureLogger with Azure Functions context
    """
    custom_attributes = {
        "azure.function.app": function_app_name,
        "azure.function.name": function_name,
        "azure.resource.type": "function",
    }

    return create_app_logger(
        service_name=f"{function_app_name}.{function_name}",
        service_version=service_version,
        connection_string=connection_string,
        custom_resource_attributes=custom_attributes,
        instrumentation_options=instrumentation_options,
    )
