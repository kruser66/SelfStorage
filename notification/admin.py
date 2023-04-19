from django.contrib import admin
from notification.models import Notify

# Register your models here.

@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    search_fields = [
        'email',
        'fullname',
    ]
    list_filter = [
        'expired_at',
        'sending_data',
        'email'
    ]