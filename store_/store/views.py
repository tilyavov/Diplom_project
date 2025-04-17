from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product, UserProfile
from django.contrib.auth.decorators import login_required

# Главная страница с каталогом товаров
def home(request):
    products = Product.objects.all()  # Получаем все товары из базы данных
    return render(request, 'store/home.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            try:
                # Попробуйте получить профиль пользователя
                user_profile = UserProfile.objects.get(user=request.user)
                product.seller = user_profile
            except UserProfile.DoesNotExist:
                # Если профиля нет, верните ошибку или создайте его (логика может быть другой)
                return render(request, 'store/add_product.html', {'form': form, 'error': 'Профиль пользователя не найден'})
            product.save()
            return redirect('home')  # Перенаправление после успешного сохранения
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request, 'store/user_profile.html', {'user_profile': user_profile})