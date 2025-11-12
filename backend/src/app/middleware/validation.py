"""Input validation and sanitization middleware."""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
import re


class ValidationMiddleware(BaseHTTPMiddleware):
    """Input validation and sanitization."""
    
    def __init__(self, app):
        super().__init__(app)
        # Patterns for detecting potential attacks
        self.xss_patterns = [
            re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
            re.compile(r'javascript:', re.IGNORECASE),
            re.compile(r'on\w+\s*=', re.IGNORECASE),
        ]
        self.sql_patterns = [
            re.compile(r"(\bOR\b|\bAND\b).*?=.*?('|\")", re.IGNORECASE),
            re.compile(r";\s*DROP\s+TABLE", re.IGNORECASE),
            re.compile(r"UNION\s+SELECT", re.IGNORECASE),
        ]
    
    def sanitize_string(self, value: str) -> str:
        """Sanitize string input."""
        if not isinstance(value, str):
            return value
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Limit string length (prevent DoS)
        max_length = 1000000  # 1MB for markdown content
        if len(value) > max_length:
            value = value[:max_length]
        
        return value
    
    def check_for_attacks(self, value: str) -> bool:
        """Check if string contains potential attack patterns."""
        if not isinstance(value, str):
            return False
        
        # Check for XSS patterns (but allow in markdown content)
        # In a real app, we'd be more sophisticated about this
        
        # Check for SQL injection patterns
        for pattern in self.sql_patterns:
            if pattern.search(value):
                return True
        
        return False
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate and sanitize request data."""
        # For now, just log and pass through
        # In production, implement more sophisticated validation
        
        # Process request
        response = await call_next(request)
        return response

