"""
Distributed tracing with OpenTelemetry
"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
import logging

logger = logging.getLogger(__name__)


def init_tracer(service_name: str, jaeger_host: str = "localhost", jaeger_port: int = 6831):
    """Initialize distributed tracing"""
    try:
        # Create resource with service name
        resource = Resource(attributes={
            "service.name": service_name
        })

        # Create tracer provider
        trace.set_tracer_provider(TracerProvider(resource=resource))

        # Configure Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=jaeger_host,
            agent_port=jaeger_port,
        )

        # Add span processor
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )

        logger.info(f"Tracing initialized for service: {service_name}")
        return trace.get_tracer(__name__)

    except Exception as e:
        logger.error(f"Failed to initialize tracing: {str(e)}")
        return None


def instrument_app(app):
    """Instrument Flask application"""
    try:
        FlaskInstrumentor().instrument_app(app)
        RequestsInstrumentor().instrument()
        logger.info("Application instrumented for tracing")
    except Exception as e:
        logger.error(f"Failed to instrument application: {str(e)}")


def instrument_sqlalchemy(engine):
    """Instrument SQLAlchemy engine"""
    try:
        SQLAlchemyInstrumentor().instrument(engine=engine)
        logger.info("SQLAlchemy instrumented for tracing")
    except Exception as e:
        logger.error(f"Failed to instrument SQLAlchemy: {str(e)}")
