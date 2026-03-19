"""Global exception handler for DRF."""
import logging
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Wrap DRF exceptions into unified {code, message, errors} format."""
    response = exception_handler(exc, context)

    if response is None:
        logger.error('Unhandled exception: %s', exc, exc_info=True)
        from rest_framework.response import Response
        return Response(
            {'code': 500, 'message': '服务器内部错误', 'errors': None},
            status=500,
        )

    code = response.status_code
    if isinstance(response.data, dict):
        message = response.data.pop('detail', str(exc))
        errors = response.data if response.data else None
    elif isinstance(response.data, list):
        message = response.data[0] if response.data else str(exc)
        errors = None
    else:
        message = str(response.data)
        errors = None

    response.data = {'code': code, 'message': str(message), 'errors': errors}
    return response
