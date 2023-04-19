from django.contrib import admin
from .models import Order, Box, Storage
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class OrderItemsInline(admin.TabularInline):
    model = Order


class BoxInline(admin.TabularInline):
    model = Box
    extra = 0

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('username', )

    inlines = [OrderItemsInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    
    inlines = [BoxInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass