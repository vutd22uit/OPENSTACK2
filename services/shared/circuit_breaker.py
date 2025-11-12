"""
Circuit breaker pattern implementation
"""
from pybreaker import CircuitBreaker, CircuitBreakerError
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class ServiceCircuitBreaker:
    """Circuit breaker for service calls"""

    def __init__(self, fail_max: int = 5, timeout_duration: int = 60):
        self.breaker = CircuitBreaker(
            fail_max=fail_max,
            timeout_duration=timeout_duration
        )

    def __call__(self, func):
        """Decorator for circuit breaker"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return self.breaker.call(func, *args, **kwargs)
            except CircuitBreakerError:
                logger.error(f"Circuit breaker open for {func.__name__}")
                raise
        return wrapper


# Global circuit breakers for each service
user_service_breaker = ServiceCircuitBreaker()
product_service_breaker = ServiceCircuitBreaker()
order_service_breaker = ServiceCircuitBreaker()
