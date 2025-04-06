from django.shortcuts import render
from .models import Product

# Главная страница с каталогом товаров
def home(request):
    products = Product.objects.all()  # Получаем все товары из базы данных
    return render(request, 'home.html', {'products': products})

# Страница товара с подробной информацией
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)  # Получаем товар по ID
    return render(request, 'product_detail.html', {'product': product})