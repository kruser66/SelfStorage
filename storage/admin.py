from django.contrib import admin
from django.utils.html import format_html
from .models import Box, Storage, Rental, Image, Order
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


def format_preview_image(image, height='200px'):
    return format_html(
        '<img src="{url}" height="{height}"/>',
        url=image.image.url,
        height=height,
    )


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


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = [format_preview_image]
    list_display = ('image', format_preview_image,)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    
    inlines = [BoxInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_filter = (
        'storage',
    )
    save_as = True
    inlines = [RentalInline, ImageInline]


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = [format_preview_image]
    list_display = ['box', format_preview_image, 'image']
    list_filter = ['box']
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass