from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from storage import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('create_order/', views.create_selfstorage_order, name='create_order'),
    path('my-rent/', views.my_rent, name='my-rent'),
    path('my-rent-empty/', views.my_rent_empty, name='my-rent-empty'),
    path('boxes/', views.boxes, name='boxes'),
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
]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
