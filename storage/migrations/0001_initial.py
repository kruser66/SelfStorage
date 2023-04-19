# Generated by Django 4.2 on 2023-04-19 12:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Этаж')),
                ('volume', models.PositiveIntegerField(verbose_name='объем')),
                ('dimension', models.CharField(default='1 x 1 x 1', max_length=20, verbose_name='Ш х В х Г')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена')),
                ('image', models.ImageField(blank=True, upload_to='images', verbose_name='Внешний вид склада')),
            ],
            options={
                'verbose_name': 'бокс',
                'verbose_name_plural': 'боксы',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес склада')),
                ('image', models.ImageField(blank=True, upload_to='images', verbose_name='Внешний вид склада')),
                ('roof_heght', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Высота потолков')),
                ('temperature', models.IntegerField(blank=True, null=True, verbose_name='Температура на складе')),
                ('benefit', models.CharField(blank=True, max_length=50, verbose_name='Преимущество')),
                ('contact', models.CharField(max_length=250, verbose_name='Контакты')),
                ('description', models.CharField(max_length=250, verbose_name='Описание')),
                ('location', models.CharField(max_length=250, verbose_name='Схема проезда')),
            ],
            options={
                'verbose_name': 'склад',
                'verbose_name_plural': 'склады',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('accepted', 'Обрабатывается'), ('done', 'Выполнен')], db_index=True, default='Обрабатывается', max_length=50, verbose_name='Статус')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий к заказу')),
                ('registered_at', models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, verbose_name='начало аренды')),
                ('end_at', models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, verbose_name='конец аренды')),
                ('pay_method', models.CharField(blank=True, choices=[('specify', 'Выяснить'), ('cash', 'Наличные'), ('card', 'Карта')], db_index=True, default='Выяснить', max_length=50, verbose_name='Способ оплаты')),
                ('box', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='storage.box', verbose_name='заказы')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='заказы')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.AddField(
            model_name='box',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boxes', to='storage.storage', verbose_name='боксы'),
        ),
    ]
