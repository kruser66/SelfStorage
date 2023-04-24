# Generated by Django 4.2 on 2023-04-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0006_alter_order_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='contact',
            field=models.CharField(blank=True, max_length=250, verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='description',
            field=models.CharField(blank=True, max_length=250, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='location',
            field=models.CharField(blank=True, max_length=250, verbose_name='Схема проезда'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='temperature',
            field=models.IntegerField(null=True, verbose_name='Температура на складе'),
        ),
    ]
