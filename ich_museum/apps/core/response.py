"""Unified API response format."""
from rest_framework.response import Response


def success_response(data=None, message='success', code=200, status=200):
    """Return a standardized success response."""
    return Response(
        {'code': code, 'message': message, 'data': data},
        status=status,
    )


def error_response(message='error', errors=None, code=400, status=400):
    """Return a standardized error response."""
    body = {'code': code, 'message': message}
    if errors:
        body['errors'] = errors
    return Response(body, status=status)
