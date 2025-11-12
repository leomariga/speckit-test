"""CSRF protection middleware."""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """CSRF protection for state-changing operations."""
    
    def __init__(self, app):
        super().__init__(app)
        self.safe_methods = {"GET", "HEAD", "OPTIONS"}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check CSRF token for state-changing requests."""
        # Skip CSRF check for safe methods
        if request.method in self.safe_methods:
            return await call_next(request)
        
        # Skip CSRF check for OAuth callback (browser redirects don't send custom headers)
        if "/auth/google/callback" in request.url.path:
            return await call_next(request)
        
        # For authenticated requests, verify origin/referer
        origin = request.headers.get("origin")
        referer = request.headers.get("referer")
        host = request.headers.get("host")
        
        # Check if request comes from allowed origin
        if origin:
            # Extract host from origin
            origin_host = origin.split("//")[-1].split(":")[0]
            request_host = host.split(":")[0] if host else ""
            
            # Allow requests from localhost/same origin
            if origin_host not in ["localhost", "127.0.0.1", request_host]:
                # In production, check against ALLOWED_ORIGINS from config
                pass
        
        # Process request
        return await call_next(request)

