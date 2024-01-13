from rest_framework import pagination


class PublicAPIPagination(pagination.PageNumberPagination):
    """Class for setting default and max pagination for the public
    API."""

    page_size = 10
    max_page_size = 40
    page_size_query_param = "size"
