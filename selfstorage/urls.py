from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from storage.views import (boxes, create_selfstorage_order, faq, index,
                           my_rent, my_rent_empty)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('faq/', faq, name='faq'),
    path('my-rent/', my_rent, name='my-rent'),
    path('my-rent-empty/', my_rent_empty, name='my-rent-empty'),
    path('boxes/', boxes, name='boxes'),
    path('create_order/', create_selfstorage_order, name='create_order'),
    path('', include('notification.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
