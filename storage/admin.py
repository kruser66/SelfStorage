from django.contrib import admin
from .models import Order, Box
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class OrderItemsInline(admin.TabularInline):
    model = Order


class BoxInline(admin.TabularInline):
    model = Box


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('username', )

    inlines = [OrderItemsInline, BoxInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Box)
