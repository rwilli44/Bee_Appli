from rest_framework import pagination


class PublicAPIPagination(pagination.PageNumberPagination):
    # pagination is set low because the DB is very small
    page_size = 5
    max_page_size = 10
    page_size_query_param = "size"
