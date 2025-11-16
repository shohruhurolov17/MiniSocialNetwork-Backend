from rest_framework.pagination import PageNumberPagination
from rest_framework import response


class CustomPagination(PageNumberPagination):

    page_size = 20
    max_page_size = 100
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        
        return response.Response({
            'success': True,
            'message': 'Data fetched successfully',
            'data': data,
            'meta': {
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'total_items': self.page.paginator.count
            }
        })