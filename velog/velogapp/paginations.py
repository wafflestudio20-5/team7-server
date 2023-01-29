from rest_framework import pagination

class PostListPagination(pagination.PageNumberPagination):
    page_size = 20

