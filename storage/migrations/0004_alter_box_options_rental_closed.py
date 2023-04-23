# Generated by Django 4.2 on 2023-04-23 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_remove_box_image_box_code_rental_price_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='box',
            options={'ordering': ['price'], 'verbose_name': 'бокс', 'verbose_name_plural': 'боксы'},
        ),
        migrations.AddField(
            model_name='rental',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='Закрыт'),
        ),
    ]