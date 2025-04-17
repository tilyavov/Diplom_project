from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Product, User, ResellerProduct, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'price', 'format', 'owner')  # Заменили 'seller' на 'owner'
    list_filter = ('genre', 'format')
    search_fields = ('name', 'description')
    ordering = ('name',)

admin.site.register(Product, ProductAdmin)

CustomUser = get_user_model()
admin.site.register(CustomUser, UserAdmin)
admin.site.register(ResellerProduct)
admin.site.register(Order)
admin.site.register(OrderItem)