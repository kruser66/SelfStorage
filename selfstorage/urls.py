from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from storage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('boxes/', views.boxes, name='boxes'),
    
    path('faq/', views.faq, name='faq'),
    path('my-rent/', views.my_rent, name='my-rent'),
    path('open-box/<int:id>', views.open_box, name='open-box'),

    path('payment_success/<pk>', views.payment_success, name='payment_success'),
    path('payment/<pk>', views.payment, name='payment'),
    
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("register", views.user_register, name="register"),
    path("edit", views.edit, name="edit"),
    path("recovery", views.recovery_password, name="recovery"),
        
]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
