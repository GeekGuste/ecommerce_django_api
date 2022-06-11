from dataclasses import field
from pyexpat import model
import this
from unicodedata import category
from matplotlib.pyplot import cla
from numpy import require
from rest_framework import serializers
from sales.models import OrderProduct
from sales.models import Order
from sales.models import DeliveryZoneInfo
from sales.models import Image
from sales.models import VariantType
from sales.models import Product 
from sales.models import Category
 
 
class DeliveryZoneInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZoneInfo
        #fields = '__all__'
        fields = ('id',
                  'zone',
                  'delivery_charges')


class CategoryCreateSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=False)
    class Meta:
        model = Category
        fields = ('id',
                  'label',
                  'image',
                  'is_active',
                  'parent_id')

 
class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    enfants = CategoryCreateSerializer(many=True)
    class Meta:
        model = Category
        #fields = '__all__'
        fields = ('id',
                  'label',
                  'image',
                  'enfants',
                  'is_active',
                  'parent')
    def get_parent(self, instance):
        if instance.parent is not None:
            return CategorySerializer(instance.parent).data
        else:
            return None


class CategoryTreeSerializer(serializers.ModelSerializer):
    enfants = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id',
                  'label',
                  'is_active',
                  'enfants')
    
    def get_enfants(self, instance):
        queryset = instance.enfants.all()
        return CategoryTreeSerializer(queryset, many=True).data


class VariantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantType
        fields = ('id',
                 'label')

class CreateProductSerializer(serializers.ModelSerializer):
    categories = CategoryCreateSerializer(required=False, many=True)
    class Meta:
        model = Product
        fields = ('id',
                  'categories',
                  'label',
                  'parent',
                  'description',
                  'qte_stock',
                  'principal_image',
                  'price',
                  'promo_price',
                  'is_variant',
                  'variant_type',
                  'variant_value',
                  'is_active')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id',
                  'photo',
                  'product')

class ProductVariantSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id',
                  'categories',
                  'variant_type',
                  'variant_value',
                  'label',
                  'images',
                  'description',
                  'qte_stock',
                  'principal_image',
                  'is_variant',
                  'price',
                  'is_variant',
                  'promo_price',
                  'pub_date')



class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    variant_type = VariantTypeSerializer(many=False)
    parent = serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True)
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id',
                  'categories',
                  'category_string',
                  'variant_type',
                  'variant_value',
                  'parent',
                  'images',
                  'variant_type',
                  'variants',
                  'label',
                  'description',
                  'qte_stock',
                  'principal_image',
                  'is_variant',
                  'price',
                  'is_variant',
                  'promo_price',
                  'pub_date')
    def get_parent(self, instance):
        if instance.parent is not None:
            return ProductSerializer(instance.parent).data
        else:
            return None
    def get_variants(self, instance):
        queryset = instance.variants.all()
        return ProductVariantSerializer(queryset, many=True).data
    def get_categories(self, instance):
        queryset = instance.categories.all()
        return CategoryCreateSerializer(queryset, many=True).data

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id',
                  'product',
                  'label',
                  'price',
                  'quantity',
                  'image_url'
                )
    def get_orderProducts(self, instance):
        queryset = instance.orderProducts.all()
        return OrderProductSerializer(queryset, many=True).data

class OrderSerializer(serializers.ModelSerializer):
    orderProducts = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id',
                  'order_date',
                  'total',
                  'country',
                  'zone',
                  'last_name',
                  'first_name',
                  'email',
                  'address',
                  'phone_number',
                  'town',
                  'postal_code',
                  'creation_date',
                  'payment_date',
                  'delivery_charges',
                  'is_delivered',
                  'user',
                  'is_paid',
                  'orderProducts'
                )
    def get_orderProducts(self, instance):
        queryset = instance.orderProducts.all()
        return OrderProductSerializer(queryset, many=True).data