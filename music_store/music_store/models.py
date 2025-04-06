from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Модель профиля пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ('musician', 'Музыкант'),
            ('label', 'Лейбл'),
            ('reseller', 'Перекупщик'),
            ('buyer', 'Покупатель'),
        ],
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

# Модель заказа
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('paid', 'Оплачен'),
        ('delivered', 'Доставлен'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Покупатель")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус заказа")
    delivery_status = models.CharField(max_length=20, choices=[('not_delivered', 'Не доставлен'), ('delivered', 'Доставлен')], default='not_delivered', verbose_name="Статус доставки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

# Модель платежа
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('completed', 'Завершен'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Статус платежа")

    def __str__(self):
        return f"Платеж для заказа #{self.order.id}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"