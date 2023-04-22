# Generated by Django 4.2 on 2023-04-21 05:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_box_busy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='image',
        ),
        migrations.AddField(
            model_name='box',
            name='code',
            field=models.ImageField(blank=True, upload_to='qr_code', verbose_name='qr'),
        ),
        migrations.AddField(
            model_name='rental',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='стоимость аренды'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rental',
            name='box',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to='storage.box', verbose_name='бокс'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='boxes', verbose_name='Изображение бокса')),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='storage.box')),
            ],
            options={
                'verbose_name': 'фотография бокса',
                'verbose_name_plural': 'фотографии боксов',
            },
        ),
    ]