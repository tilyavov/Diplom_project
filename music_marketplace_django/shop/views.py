from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import RegistrationForm, LoginForm, ProductForm, EditProfileForm # Изменено: импортируем EditProfileForm
from .models import Product, User

def index(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(owner=request.user)
    else:
        products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт для {user.username} успешно создан! Теперь вы можете войти.')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'shop/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def errorautation(request):
    products = Product.objects.all()
    return render(request, 'shop/errorautation.html', {'products': products})

@login_required(login_url='errorautation')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('index')
        else:
            return render(request, 'shop/add_product.html', {'form': form})
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required(login_url='errorautation')
def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user) # Добавляем request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка при обновлении профиля.')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'shop/profile.html', {'form': form})

@login_required(login_url='errorautation')
def my_products(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, 'shop/my_products.html', {'products': products})

@login_required(login_url='errorautation')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлен!')
            return redirect('my_products')
        else:
            messages.error(request, 'Ошибка при обновлении товара.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form})

@login_required(login_url='errorautation')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, owner=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар успешно удален!')
        return redirect('my_products')
    return render(request, 'shop/delete_confirm.html', {'product': product})