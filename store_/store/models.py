from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Модель профиля пользователя
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('musician', 'Музыкант'),
        ('label', 'Лейбл'),
        ('reseller', 'Перекупщик'),
        ('buyer', 'Покупатель'),
    ]
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='buyer'
    )
    is_reseller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

# Модель товара
class Product(models.Model):
    SELLER_TYPE_CHOICES = [
        ('musician', 'Музыкант'),
        ('label', 'Лейбл'),
        ('reseller', 'Перекупщик'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    genre = models.CharField(max_length=50, verbose_name="Жанр")
    seller_type = models.CharField(max_length=20, choices=SELLER_TYPE_CHOICES, verbose_name="Тип продавца")
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Продавец")
    is_original = models.BooleanField(default=True, verbose_name="Оригинальный товар")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"