"""Request logging middleware."""
import logging
import time

logger = logging.getLogger('apps.core.middleware')


class RequestLoggingMiddleware:
    """Log every API request with method, path, user, status, and duration."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000

        user_id = getattr(request.user, 'id', 'anonymous')
        level = logging.WARNING if response.status_code >= 400 else logging.INFO
        logger.log(
            level,
            '%s %s user=%s status=%d %.0fms',
            request.method, request.path, user_id,
            response.status_code, duration_ms,
        )
        return response
