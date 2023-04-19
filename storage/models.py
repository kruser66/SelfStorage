from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Storage(models.Model):
    city = models.CharField(
        'Город',
        max_length=100       
    )
    address = models.CharField(
        'Адрес склада',
        max_length=200
    )
    image= models.ImageField(
        'Внешний вид склада',
        upload_to='images',
        blank=True
    )
    roof_heght = models.DecimalField(
        'Высота потолков',
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)]
    )
    temperature = models.IntegerField('Температура на складе', blank=True, null=True)
    benefit = models.CharField(
        'Преимущество',
        max_length=50,
        blank=True
    )
    contact = models.CharField('Контакты', max_length=250)
    description = models.CharField('Описание', max_length=250)
    location = models.CharField('Схема проезда', max_length=250)  # TODO сделать карту пока просто текстом

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'

    def __str__(self):
        return f'{self.city} {self.address}'


class Box(models.Model):
    storage = models.ForeignKey(
        Storage,
        related_name='boxes',
        verbose_name="боксы",
        on_delete=models.CASCADE,
    )
    floor = models.PositiveSmallIntegerField('Этаж', null=True, blank=True)
    volume = models.PositiveIntegerField('объем')
    dimension = models.CharField('Ш х В х Г', max_length=20, default='1 x 1 x 1')
    price = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image= models.ImageField(
        'Изображение боксов',
        upload_to='images',
        blank=True
    )
    # feature = models.CharField(
    #     'Особенность',
    #     max_length=200,
    #     blank=True,
    #     db_index=True,
    # )
    # # temperature = models.IntegerField('температура')
    # code = models.ImageField('qr', blank=True, upload_to='qr_code')

    class Meta:
        verbose_name = 'бокс'
        verbose_name_plural = 'боксы'

    def __str__(self):
        return f'{self.address}-{self.volume}--{self.dimension}--{self.price}'

    # def save(self, *args, **kwargs):
    #     qr_image = qrcode.make(f'{self.client.get_full_name} - {self.address} - {self.size}')
    #     qr_offset = Image.new('RGB', (310, 310), 'white')
    #     qr_offset.paste(qr_image)
    #     files_name = f'{self.client.get_full_name}-{self.id}qr.png'
    #     stream = BytesIO()
    #     qr_offset.save(stream, 'PNG')
    #     self.code.save(files_name, File(stream), save=False)
    #     qr_offset.close
    #     super().save(*args, **kwargs)


class Order(models.Model):
    ORDER_STATE_CHOICES = [
        ('accepted', 'Обрабатывается'),
        ('done', 'Выполнен')
    ]
    PAYMENT_CHOICES = [
        ('specify', 'Выяснить'),
        ('cash', 'Наличные'),
        ('card', 'Карта')
    ]
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
