# Generated by Django 4.2 on 2023-04-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='Имя клиента')),
                ('email', models.EmailField(max_length=254)),
                ('sending_data', models.DateField(db_index=True, verbose_name='Плановая дата отправки')),
                ('subject', models.CharField(max_length=200, verbose_name='Тема сообщения')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
                ('rental_info', models.CharField(max_length=200, verbose_name='Информация о заказе')),
                ('expired_at', models.DateField(db_index=True, verbose_name='Срок окончания заказа')),
                ('executed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'уведомление',
                'verbose_name_plural': 'уведомления',
            },
        ),
    ]
