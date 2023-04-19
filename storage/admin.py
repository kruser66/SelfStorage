from django.contrib import admin
from .models import Box, Storage, Rental
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class BoxInline(admin.TabularInline):
    model = Box
    extra = 0

class RentalInline(admin.TabularInline):
    model = Rental
    extra = 0

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('username', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    
    inlines = [BoxInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_filter = (
        'storage',
    )
    save_as = True
    inlines = [RentalInline]


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    pass