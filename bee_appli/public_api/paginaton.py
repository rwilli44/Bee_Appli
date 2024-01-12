from rest_framework import pagination


class PublicAPIPagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 40
    page_size_query_param = "size"
