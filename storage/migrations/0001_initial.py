# Generated by Django 4.2 on 2023-04-18 13:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(max_length=50)),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, max_length=128, null=True, region=None, verbose_name='телефон')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accepted', 'Обрабатывается'), ('done', 'Выполнен')], db_index=True, default='Обрабатывается', max_length=50, verbose_name='Статус')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий к заказу')),
                ('registered_at', models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, verbose_name='Время регистрации')),
                ('pay_method', models.CharField(choices=[('specify', 'Выяснить'), ('cash', 'Наличные'), ('card', 'Карта')], db_index=True, default='Выяснить', max_length=50, verbose_name='Способ оплаты')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='storage.client', verbose_name='заказы')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]
