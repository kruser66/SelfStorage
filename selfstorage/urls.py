from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from storage import views

from storage.views import (boxes, create_selfstorage_order, faq, index,
                           my_rent, my_rent_empty)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('my-rent/', views.my_rent, name='my-rent'),
    path('my-rent-empty/', views.my_rent_empty, name='my-rent-empty'),
    path('boxes/', views.boxes, name='boxes'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('notification.urls')),
    # login/logout
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path(
        "logout",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
    path("account", views.account, name="account"),
]
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
