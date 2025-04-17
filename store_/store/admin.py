from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'genre', 'seller')
    search_fields = ('name', 'genre')
    list_filter = ('genre', 'seller_type')