from rest_framework import pagination

class StandardResultPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'