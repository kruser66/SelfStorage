from django.contrib import admin
from .models import Box, Storage, Rental
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class BoxInline(admin.TabularInline):
    model = Box
    extra = 0


class RentalInline(admin.TabularInline):
    model = Rental
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phonenumber",
                    "avatar",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)


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