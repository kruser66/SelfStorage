from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from storage.views import boxes, faq, index, my_rent, my_rent_empty

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('faq/', faq, name='faq'),
    path('my-rent/', my_rent, name='my-rent'),
    path('my-rent-empty/', my_rent_empty, name='my-rent-empty'),
    path('boxes/', boxes, name='boxes'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('notification.urls'))
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
