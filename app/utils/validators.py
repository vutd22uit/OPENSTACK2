"""
Input validation and sanitization utilities
"""
import re
import html
from typing import Any

def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent XSS attacks
    """
    if not isinstance(input_string, str):
        return str(input_string)

    # HTML escape
    sanitized = html.escape(input_string)

    # Remove any potential script tags or dangerous patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
    ]

    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)

    return sanitized.strip()

def validate_input(input_string: str, min_length: int = 1,
                   max_length: int = 255, pattern: str = None) -> bool:
    """
    Validate input string against constraints
    """
    if not isinstance(input_string, str):
        return False

    # Length validation
    if len(input_string) < min_length or len(input_string) > max_length:
        return False

    # Pattern validation if provided
    if pattern and not re.match(pattern, input_string):
        return False

    return True

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_alphanumeric(input_string: str) -> bool:
    """Validate alphanumeric input"""
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', input_string))
