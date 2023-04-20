from io import BytesIO

import qrcode
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files import File
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    phonenumber = PhoneNumberField("телефон", db_index=True, blank=True)
    avatar = models.ImageField("аватарка", blank=True)
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Storage(models.Model):
    city = models.CharField(
        'Город',
        max_length=100       
    )
    address = models.CharField(
        'Адрес склада',
        max_length=200
    )
    image = models.ImageField(
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
    busy = models.BooleanField(
        'Бокс занят',
        db_index=True,
        default=False
    )
    code = models.ImageField('qr', blank=True, upload_to='qr_code')

    def open(self):
        if not self.busy:
            raise ValueError("Бокс уже открыт")
        self.busy = False
        self.save()
        return True

    class Meta:
        verbose_name = 'бокс'
        verbose_name_plural = 'боксы'

    def __str__(self):
        return f'{self.storage} -- {self.volume} м3 -- {self.dimension} м -- {self.price} руб.'

    # def save(self, *args, **kwargs):
    #     qr_image = qrcode.make(f'{self.storage} - {self.volume} - {self.dimension}')
    #     qr_offset = Image.new('RGB', (512, 512), 'white')
    #     qr_offset.paste(qr_image)
    #     files_name = f'{self.storage}-{self.id}qr.png'
    #     stream = BytesIO()
    #     qr_offset.save(stream, 'PNG')
    #     self.code.save(files_name, File(stream), save=False)
    #     qr_offset.close
    #     super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField('Изображение бокса', blank=True, upload_to='boxes')
    box = models.ForeignKey(Box, related_name='images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'фотография бокса'
        verbose_name_plural = 'фотографии боксов'


    def __str__(self):
        return f'{self.box.storage}'


class Rental(models.Model):
    client = models.ForeignKey(
        User,
        related_name='rents',
        verbose_name="клиент",
        on_delete=models.CASCADE,
    )
    box = models.ForeignKey(
        Box,
        related_name='rents',
        verbose_name="бокс",
        on_delete=models.CASCADE,
    )
    comment = models.TextField('Комментарий к заказу', blank=True)
    started_at = models.DateField(
        'начало аренды',
        auto_now_add=True,
        db_index=True,
    )
    expired_at = models.DateField(
        'конец аренды',
        null=True,
        blank=True,
        db_index=True,
    )
    paid = models.BooleanField('Оплачен', default=False)
    price = models.DecimalField(
        'стоимость аренды',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        verbose_name = 'договор аренды'
        verbose_name_plural = 'договора аренды'
        ordering = ['-expired_at']

    def __str__(self):
        return f'{self.client} срок окончания: {self.expired_at}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'Новый'),
        ('PAID', 'Оплачен'),
        ('CANCELED', 'Отменен'),
    )

<<<<<<< HEAD
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
=======
    user = models.ForeignKey(User,
        related_name='orders',
        verbose_name="заказы",
        on_delete=models.CASCADE
    )
>>>>>>> 6c680c5 (fix order and html)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Заказ #{self.pk} - {self.description}'
