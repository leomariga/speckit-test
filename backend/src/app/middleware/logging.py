"""Request logging middleware."""
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request and response details."""
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        method = request.method
        path = request.url.path
        
        print(f"[{request_id}] {method} {path} - Started")
        
        # Process request
        try:
            response = await call_next(request)
            
            # Log response
            duration = time.time() - start_time
            status_code = response.status_code
            
            print(
                f"[{request_id}] {method} {path} - "
                f"Completed {status_code} in {duration:.3f}s"
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            print(
                f"[{request_id}] {method} {path} - "
                f"Failed with error: {str(e)} in {duration:.3f}s"
            )
            raise

