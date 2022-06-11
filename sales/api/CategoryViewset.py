import re
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from sales.models import Category
from sales.serializers import CategorySerializer, CategoryCreateSerializer, CategoryTreeSerializer
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CategoryViewset(ModelViewSet):
    #To return all objects
    pagination_class = StandardResultsSetPagination
    serializer_class = CategorySerializer
    create_serializer_class = CategoryCreateSerializer
    tree_serializer_class = CategoryTreeSerializer
    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update":
            return self.create_serializer_class
        if self.action == "tree":
            return self.tree_serializer_class
        return super().get_serializer_class()
    
    @action(detail=False, methods=['get'], url_path="tree")
    def tree(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)