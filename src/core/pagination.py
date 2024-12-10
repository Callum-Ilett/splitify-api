"""Pagination classes."""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination class for standard results set."""

    page_size = 10
    page_size_query_param = "limit"
