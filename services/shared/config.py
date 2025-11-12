"""
Shared configuration for microservices
"""
import os
from typing import Optional
from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    """Base configuration for all services"""

    # Service Info
    SERVICE_NAME: str = Field(..., env="SERVICE_NAME")
    SERVICE_VERSION: str = Field("1.0.0", env="SERVICE_VERSION")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")

    # Server
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(5000, env="PORT")
    DEBUG: bool = Field(False, env="DEBUG")

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_POOL_SIZE: int = Field(10, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(20, env="DB_MAX_OVERFLOW")

    # Redis
    REDIS_URL: str = Field("redis://localhost:6379", env="REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")

    # RabbitMQ
    RABBITMQ_URL: str = Field("amqp://guest:guest@localhost:5672/", env="RABBITMQ_URL")

    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_EXPIRATION_DELTA: int = Field(3600, env="JWT_EXPIRATION_DELTA")  # 1 hour

    # CORS
    CORS_ORIGINS: str = Field("*", env="CORS_ORIGINS")

    # Observability
    JAEGER_AGENT_HOST: str = Field("localhost", env="JAEGER_AGENT_HOST")
    JAEGER_AGENT_PORT: int = Field(6831, env="JAEGER_AGENT_PORT")
    ENABLE_TRACING: bool = Field(True, env="ENABLE_TRACING")

    # Service Discovery
    CONSUL_HOST: str = Field("localhost", env="CONSUL_HOST")
    CONSUL_PORT: int = Field(8500, env="CONSUL_PORT")

    # Circuit Breaker
    CIRCUIT_BREAKER_FAIL_MAX: int = Field(5, env="CIRCUIT_BREAKER_FAIL_MAX")
    CIRCUIT_BREAKER_TIMEOUT: int = Field(60, env="CIRCUIT_BREAKER_TIMEOUT")

    class Config:
        case_sensitive = True
        env_file = ".env"


def get_config() -> BaseConfig:
    """Get configuration instance"""
    return BaseConfig()
