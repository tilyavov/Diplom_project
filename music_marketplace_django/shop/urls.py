from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views # Если вы используете стандартный логаут Django
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('errorautation/', views.errorautation, name='errorautation'),
    #path('layout/', views.layout, name='layout'),  # Добавляем URL для layout
    path('add_product/', views.add_product, name='add_product'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('my_products/', views.my_products, name='my_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)