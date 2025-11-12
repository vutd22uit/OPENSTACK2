"""
Shared configuration for microservices - simplified version
"""
import os
from typing import Optional


class BaseConfig:
    """Base configuration for all services"""

    def __init__(self):
        # Service Info
        self.SERVICE_NAME = os.getenv('SERVICE_NAME', 'unknown-service')
        self.SERVICE_VERSION = os.getenv('SERVICE_VERSION', '1.0.0')
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

        # Server
        self.HOST = os.getenv('HOST', '0.0.0.0')
        self.PORT = int(os.getenv('PORT', 5000))
        self.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

        # Database
        self.DATABASE_URL = os.getenv('DATABASE_URL', '')
        self.DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 10))
        self.DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', 20))

        # Redis
        self.REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

        # RabbitMQ
        self.RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

        # Security
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
        self.JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
        self.JWT_EXPIRATION_DELTA = int(os.getenv('JWT_EXPIRATION_DELTA', 3600))

        # CORS
        self.CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

        # Observability
        self.JAEGER_AGENT_HOST = os.getenv('JAEGER_AGENT_HOST', 'localhost')
        self.JAEGER_AGENT_PORT = int(os.getenv('JAEGER_AGENT_PORT', 6831))
        self.ENABLE_TRACING = os.getenv('ENABLE_TRACING', 'false').lower() == 'true'

        # Service Discovery
        self.CONSUL_HOST = os.getenv('CONSUL_HOST', 'localhost')
        self.CONSUL_PORT = int(os.getenv('CONSUL_PORT', 8500))

        # Circuit Breaker
        self.CIRCUIT_BREAKER_FAIL_MAX = int(os.getenv('CIRCUIT_BREAKER_FAIL_MAX', 5))
        self.CIRCUIT_BREAKER_TIMEOUT = int(os.getenv('CIRCUIT_BREAKER_TIMEOUT', 60))


def get_config() -> BaseConfig:
    """Get configuration instance"""
    return BaseConfig()
