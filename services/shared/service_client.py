"""
HTTP client for inter-service communication
"""
import requests
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)


class ServiceClient:
    """HTTP client for calling other microservices"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def get(self, endpoint: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request with retry"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"GET request failed: {url}, error: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def post(self, endpoint: str, data: Dict[str, Any], headers: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request with retry"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"POST request failed: {url}, error: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def put(self, endpoint: str, data: Dict[str, Any], headers: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT request with retry"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.put(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"PUT request failed: {url}, error: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """DELETE request with retry"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.delete(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.RequestException as e:
            logger.error(f"DELETE request failed: {url}, error: {str(e)}")
            raise
