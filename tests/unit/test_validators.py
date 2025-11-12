"""
Unit tests for validators
"""
import pytest
from app.utils.validators import (
    sanitize_input,
    validate_input,
    validate_email,
    validate_alphanumeric
)

class TestSanitizeInput:
    """Test input sanitization"""

    def test_sanitize_script_tags(self):
        """Test removal of script tags"""
        dirty = '<script>alert("xss")</script>Hello'
        clean = sanitize_input(dirty)
        assert '<script>' not in clean.lower()

    def test_sanitize_html_entities(self):
        """Test HTML entity escaping"""
        dirty = '<div>Test & "quotes"</div>'
        clean = sanitize_input(dirty)
        assert '&lt;' in clean or '<div>' not in clean

    def test_sanitize_javascript_protocol(self):
        """Test removal of javascript: protocol"""
        dirty = 'javascript:alert(1)'
        clean = sanitize_input(dirty)
        assert 'javascript:' not in clean.lower()

class TestValidateInput:
    """Test input validation"""

    def test_validate_length(self):
        """Test length validation"""
        assert validate_input('test', min_length=1, max_length=10)
        assert not validate_input('', min_length=1, max_length=10)
        assert not validate_input('a' * 100, min_length=1, max_length=10)

    def test_validate_pattern(self):
        """Test pattern validation"""
        pattern = r'^[a-zA-Z]+$'
        assert validate_input('abc', pattern=pattern)
        assert not validate_input('abc123', pattern=pattern)

class TestValidateEmail:
    """Test email validation"""

    def test_valid_email(self):
        """Test valid email addresses"""
        assert validate_email('user@example.com')
        assert validate_email('user.name@example.co.uk')

    def test_invalid_email(self):
        """Test invalid email addresses"""
        assert not validate_email('invalid')
        assert not validate_email('@example.com')
        assert not validate_email('user@')

class TestValidateAlphanumeric:
    """Test alphanumeric validation"""

    def test_valid_alphanumeric(self):
        """Test valid alphanumeric strings"""
        assert validate_alphanumeric('abc123')
        assert validate_alphanumeric('test_name-123')

    def test_invalid_alphanumeric(self):
        """Test invalid alphanumeric strings"""
        assert not validate_alphanumeric('test@example')
        assert not validate_alphanumeric('test space')
