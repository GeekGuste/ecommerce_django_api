from django.contrib import admin
from sales.models import Product
from sales.models import Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
