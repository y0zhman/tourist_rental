from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Категория снаряжения (палатки, спальники и т.д.)"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-имя'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Единица туристического снаряжения"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='equipment',
        verbose_name='Категория'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за день (₽)'
    )
    deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Залог (₽)'
    )
    image = models.ImageField(
        upload_to='equipment/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    quantity_total = models.PositiveIntegerField(
        default=1,
        verbose_name='Всего единиц'
    )
    quantity_available = models.PositiveIntegerField(
        default=1,
        verbose_name='Доступно единиц'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Снаряжение'
        verbose_name_plural = 'Снаряжение'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def is_available(self):
        """Проверка: доступно ли снаряжение сейчас"""
        return self.is_active and self.quantity_available > 0


class Booking(models.Model):
    """Бронирование снаряжения пользователем"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('active', 'Активно'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Пользователь'
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Снаряжение'
    )
    start_date = models.DateField(
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        verbose_name='Дата окончания'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая стоимость (₽)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.equipment.name} ({self.start_date} — {self.end_date})'

    def days_count(self):
        """Количество дней аренды"""
        return (self.end_date - self.start_date).days + 1