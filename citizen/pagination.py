from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings


class CustomListPagination(PageNumberPagination):
    page_size = api_settings.PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'page_size'