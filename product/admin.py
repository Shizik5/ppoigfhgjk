from django.contrib import admin
from product.models import Category, Product, CartItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)