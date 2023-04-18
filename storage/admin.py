from django.contrib import admin
from models import Client,  Order


class OrderItemsInline(admin.TabularInline):
    model = Order


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = [
        'email',
        'username',
        'password',
        'phonenumber',
    ]

    inlines = [OrderItemsInline, ]
