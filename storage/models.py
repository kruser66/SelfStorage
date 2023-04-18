from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class Client(models.Model):
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=50)
    phonenumber = PhoneNumberField(
        'телефон',
        db_index=True,
        blank=True,
        null=True,
    )


class Order(models.Model):
    client = models.ForeignKey(
        Client,
        related_name='orders',
        verbose_name="заказы",
        on_delete=models.CASCADE,
    )
    ORDER_STATE_CHOICES = [
        ('accepted', 'Обрабатывается'),
        ('done', 'Выполнен')
    ]
    PAYMENT_CHOICES = [
        ('specify', 'Выяснить'),
        ('cash', 'Наличные'),
        ('card', 'Карта')
    ]
    status = models.CharField(
        'Статус',
        max_length=50,
        choices=ORDER_STATE_CHOICES,
        default='Обрабатывается',
        db_index=True
    )
    comment = models.TextField('Комментарий к заказу', blank=True)
    registered_at = models.DateTimeField(
        'Время регистрации',
        default=timezone.now,
        blank=True,
        db_index=True
    )
    pay_method = models.CharField(
        'Способ оплаты',
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='Выяснить',
        db_index=True
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.status} {self.registered_at}'
