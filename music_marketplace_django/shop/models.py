from django.db import models
from django.contrib.auth.models import AbstractUser  # Import AbstractUser
from django.conf import settings  # Import settings


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_reseller = models.BooleanField(default=False)

    role_choices = [
        ('buyer', 'Покупатель'),
        ('musician', 'Музыкант'),
        ('label', 'Лейбл'),
        ('reseller', 'Перекупщик'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=20, choices=role_choices, default='buyer')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="shop_users_groups",  # Changed related_name
        related_query_name="shop_user",    # Changed related_query_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="shop_users_permissions", # Changed related_name
        related_query_name="shop_user",      # Changed related_query_name
    )

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField()
    genre = models.CharField(max_length=50, blank=True)
    format_choices = [
        ('CD', 'CD'),
        ('Vinyl', 'Винил'),
        ('Cassette', 'Кассета'),
    ]
    format = models.CharField(max_length=50, choices=format_choices)
    is_original = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')  # Renamed 'seller' to 'owner'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ResellerProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reseller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reseller_products')
    reseller_price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} (перепродажа {self.reseller.username})"

    class Meta:
        verbose_name = 'Перепродаваемый продукт'
        verbose_name_plural = 'Перепродаваемые продукты'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()  # Цена товара на момент заказа

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в заказе №{self.order.id}"

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'