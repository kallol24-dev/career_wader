from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default
    page_size_query_param = 'page_size'  # Allow clients to override
    max_page_size = 100  # Optional: limit max value