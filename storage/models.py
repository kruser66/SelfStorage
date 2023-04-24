from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

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
    date_joined = models.DateTimeField(_("date joined"), default=now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

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
    temperature = models.IntegerField('Температура на складе', null=True)
    benefit = models.CharField(
        'Преимущество',
        max_length=50,
        blank=True
    )
    contact = models.CharField('Контакты', max_length=250, blank=True)
    description = models.CharField('Описание', max_length=250, blank=True)
    location = models.CharField('Схема проезда', max_length=250, blank=True)  # TODO сделать карту пока просто текстом

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'

    def __str__(self):
        return f'{self.city} {self.address}'

    def get_volume_all(self):
        return self.boxes.filter(busy=False)

    def get_volume_to3(self):
        return self.boxes.filter(volume__lt=3, busy=False)

    def get_volume_to10(self):
        return self.boxes.filter(volume__lt=10, busy=False)

    def get_volume_from10(self):
        return self.boxes.filter(volume__gte=10, busy=False)


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

    class Meta:
        verbose_name = 'бокс'
        verbose_name_plural = 'боксы'
        ordering = ['price']

    def __str__(self):
        return f'{self.storage} -- {self.volume} м3 -- {self.dimension} м -- {self.price} руб.'
    
    def open(self):
        if not self.busy:
            raise ValueError("Бокс уже открыт")
        self.busy = False
        self.save()
        return True


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
    closed = models.BooleanField('Закрыт', default=False)
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

    def is_expired_soon(self):
        return self.expired_at - timedelta(days=10) < now().date()
    
    def is_expired(self):
        return now().date() > self.expired_at


class Order(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'Новый'),
        ('PAID', 'Оплачен'),
        ('CANCELED', 'Отменен'),
    )
    payment_id = models.CharField(max_length=36, default='0')
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='boxes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    description = models.TextField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'счет'
        verbose_name_plural = 'счета'

    def __str__(self):
        return f'Заказ #{self.pk} - {self.description}'
