"""Pagination classes."""
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class _EnvelopeMixin:
    """Wrap paginated response in {code, message, data} envelope."""

    def get_paginated_response(self, data):
        return Response({
            'code': 200,
            'message': 'success',
            'data': OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
            ]),
        })


class StandardPagination(_EnvelopeMixin, PageNumberPagination):
    """Default pagination: 12 items per page."""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdminPagination(_EnvelopeMixin, PageNumberPagination):
    """Admin pagination: 20 items per page."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
