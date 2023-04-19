
from django.urls import path

from notification.views import send_email


urlpatterns = [
    path('notify/', send_email)
]