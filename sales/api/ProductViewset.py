from cProfile import label
from functools import reduce
import json
from unicodedata import category
from numpy import product
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from sales.models import Order
from sales.serializers import OrderSerializer
from sales.models import Category
from sales.models import Image
from sales.models import Product, VariantType
from sales.serializers import ProductSerializer, CreateProductSerializer, VariantTypeSerializer, ImageSerializer
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import operator

class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    create_serializer_class = CreateProductSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        newProduct = Product(
            is_active = data["is_active"],
            label = data["label"],
            description = data["description"],
            qte_stock = data["qte_stock"],
            principal_image = data["principal_image"] if "principal_image" in data else None,
            is_variant = data["is_variant"] if "is_variant" in data else None,
            variant_value = data["variant_value"] if "variant_value" in data else None,
            parent = Product.objects.get(pk=data["parent"]) if "parent" in data else None,
            price = data["price"],
            promo_price = data["promo_price"]
        )
        newProduct.save()
        if "categories" in data and data["categories"]:
            categories = data["categories"].split(",")
            if categories:
                for categoryId in data["categories"].split(","):
                    category = Category.objects.get(pk=categoryId)
                    newProduct.categories.add(category)
                    newProduct.category_string += (category.getTreeNames() + " ")
                newProduct.save()
        serializer = CreateProductSerializer(newProduct)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        product = self.get_object()
        if "label" in data:
            product.label = data["label"]
        if "description" in data:
            product.description = data["description"]
        if "qte_stock" in data:
            product.qte_stock = data["qte_stock"]
        if "principal_image" in data:
            product.principal_image = data["principal_image"]
        if "price" in data:
            product.price = data["price"]
        if "promo_price" in data:
            product.promo_price = data["promo_price"]
        if "variant_type" in data:
            variantType = VariantType.objects.get(pk=data["variant_type"]) if data["variant_type"] is not None else None
            product.variant_type = variantType
            product.save()
        if "categories" in data:
            #clear categories to update later
            product.categories.clear()
            categories = data["categories"].split(",")
            if categories:
                for categoryId in categories:
                    category = Category.objects.get(pk=categoryId)
                    product.categories.add(category)
                product.save()
        serializer = CreateProductSerializer(product)
        return Response(serializer.data)
    def get_queryset(self):
        queryset = Product.objects
        category_id = self.request.GET.get('category')
        if category_id is not None:
            #queryset = queryset.filter(category__id=category_id)
            category = Category.objects.get(pk=category_id)
            queryset = queryset.filter(category_string__contains=category.label)
        is_variant = self.request.GET.get('is_variant')
        if is_variant is not None:
            queryset = queryset.filter(is_variant=is_variant)
        search_text = self.request.GET.get('search_text')
        if search_text is not None:
            list = search_text.split()
            queryset = queryset.filter(reduce(operator.or_, ((Q(label__contains=x) | Q(description__contains=x) | Q(category_string__contains=x)) for x in list)))
        return queryset

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update":
            return self.create_serializer_class
        return super().get_serializer_class()

class ImageViewset(ModelViewSet):
    serializer_class = ImageSerializer
    def get_queryset(self):
        return Image.objects.all()
    
    @action(detail=True, methods=['put'], url_path="remove")
    def remove(self, request, pk):
        image = self.get_object()
        image.delete()
        return Response(image)
        
class VariantTypeViewset(ModelViewSet):
    serializer_class = VariantTypeSerializer
    def get_queryset(self):
        return VariantType.objects.all()

class OrderViewset(ModelViewSet):
    serializer_class = OrderSerializer
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by("-order_date")
        return queryset
    @action(detail=False, methods=['get'], url_path="all")
    def all(self, request):
        queryset = Order.objects.order_by("-order_date")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)