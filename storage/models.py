from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Box(models.Model):
    client = models.ForeignKey(
        User,
        related_name='boxes',
        verbose_name="боксы",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        db_index=True,
    )
    size = models.PositiveIntegerField('объем')
    price = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    feature = models.CharField(
        'Особенность',
        max_length=200,
        blank=True,
        db_index=True,
    )
    temperature = models.IntegerField('температура')

    class Meta:
        verbose_name = 'бокс'
        verbose_name_plural = 'боксы'

    def __str__(self):
        return f'{self.address}-{self.size}-{self.price}-{self.feature}'

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(f'{self.client.get_full_name} - {self.address} - {self.size}')
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.client.get_full_name}-{self.id}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.code.save(files_name, File(stream), save=False)
        qr_offset.close
        super().save(*args, **kwargs)


class Order(models.Model):
    client = models.ForeignKey(
        User,
        related_name='orders',
        verbose_name="заказы",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    box = models.ForeignKey(
        Box,
        related_name='orders',
        verbose_name="заказы",
        blank=True,
        null=True,
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
        blank=True,
        db_index=True
    )
    comment = models.TextField('Комментарий к заказу', blank=True)
    registered_at = models.DateTimeField(
        'начало аренды',
        default=timezone.now,
        blank=True,
        db_index=True,
    )
    end_at = models.DateTimeField(
        'конец аренды',
        default=timezone.now,
        blank=True,
        db_index=True,
    )
    pay_method = models.CharField(
        'Способ оплаты',
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='Выяснить',
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.status} {self.registered_at}'
