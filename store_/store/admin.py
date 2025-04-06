from django.contrib import admin
from .models import UserProfile, Product, Order, Payment

# Регистрация моделей в админке
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Payment)