"""Telemetry and observability for StepChain.

This module provides OpenTelemetry integration with JSON fallback.
"""

import json
import logging
import os
import sys
from collections.abc import Iterator
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from typing import Any, TextIO

logger = logging.getLogger(__name__)


class JSONExporter:
    """Fallback JSON line exporter for telemetry."""

    def __init__(self, output_file: str | None = None):
        """Initialize JSON exporter.

        Args:
            output_file: Path to output file (defaults to stderr)
        """
        self.output_file = output_file
        self._file: TextIO | None = None

    def export(self, span_data: dict[str, Any]) -> None:
        """Export span data as JSON line."""
        if self.output_file:
            if not self._file:
                self._file = open(self.output_file, "a")  # noqa: SIM115
            self._file.write(json.dumps(span_data) + "\n")
            self._file.flush()
        else:
            print(json.dumps(span_data), file=sys.stderr)

    def close(self) -> None:
        """Close the output file if open."""
        if self._file:
            self._file.close()


class Telemetry:
    """Telemetry manager with OTLP and JSON fallback.

    Example:
        >>> telemetry = Telemetry()
        >>> with telemetry.span("process_data", {"size": 1024}):
        ...     # Process data
        ...     pass
    """

    def __init__(self, service_name: str = "taskcrew-segmenter"):
        """Initialize telemetry.

        Args:
            service_name: Name of the service for telemetry
        """
        self.service_name = service_name
        self.tracer: Any = None
        self.json_exporter: JSONExporter | None = None
        
        # Try to initialize OTLP
        if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
            try:
                self._init_otlp()
            except Exception as e:
                logger.warning(f"Failed to initialize OTLP, falling back to JSON: {e}")
                self._init_json_fallback()
        else:
            self._init_json_fallback()

    def _init_otlp(self) -> None:
        """Initialize OpenTelemetry with OTLP exporter."""
        try:
            from opentelemetry import trace
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            resource = Resource.create({"service.name": self.service_name})
            provider = TracerProvider(resource=resource)
            
            otlp_exporter = OTLPSpanExporter()
            span_processor = BatchSpanProcessor(otlp_exporter)
            provider.add_span_processor(span_processor)
            
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer(__name__)
            logger.info("Initialized OTLP telemetry")
        except ImportError:
            raise ImportError("OTLP support requires opentelemetry-exporter-otlp") from None

    def _init_json_fallback(self) -> None:
        """Initialize JSON fallback exporter."""
        output_file = os.environ.get("TELEMETRY_JSON_FILE")
        self.json_exporter = JSONExporter(output_file)
        logger.info(f"Initialized JSON telemetry (output: {output_file or 'stderr'})")

    @contextmanager
    def span(self, name: str, attributes: dict[str, Any] | None = None) -> Iterator[None]:
        """Create a telemetry span.

        Args:
            name: Span name
            attributes: Span attributes

        Example:
            >>> with telemetry.span("api_call", {"endpoint": "/users"}):
            ...     make_api_call()
        """
        start_time = datetime.utcnow()
        
        if self.tracer:
            with self.tracer.start_as_current_span(name, attributes=attributes):
                yield
        else:
            # JSON fallback
            try:
                yield
            finally:
                end_time = datetime.utcnow()
                duration_ms = (end_time - start_time).total_seconds() * 1000
                
                span_data = {
                    "timestamp": start_time.isoformat(),
                    "name": name,
                    "duration_ms": duration_ms,
                    "attributes": attributes or {},
                    "service": self.service_name,
                }
                
                if self.json_exporter:
                    self.json_exporter.export(span_data)

    @asynccontextmanager
    async def async_span(self, name: str, attributes: dict[str, Any] | None = None):
        """Create an async telemetry span."""
        with self.span(name, attributes):
            yield

    def record_error(self, error: Exception, attributes: dict[str, Any] | None = None) -> None:
        """Record an error in telemetry."""
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error": {
                "type": type(error).__name__,
                "message": str(error),
            },
            "attributes": attributes or {},
            "service": self.service_name,
        }
        
        if self.json_exporter:
            self.json_exporter.export(error_data)

    def close(self) -> None:
        """Close telemetry resources."""
        if self.json_exporter:
            self.json_exporter.close()
