# Generated by Django 4.2 on 2023-04-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_rental_alter_box_image_delete_order_rental_box_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='expired_at',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='конец аренды'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='start_at',
            field=models.DateField(auto_now_add=True, db_index=True, verbose_name='начало аренды'),
        ),
    ]
