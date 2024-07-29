from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from shop import views as shop_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('register/', auth_views.LoginView.as_view(template_name='shop/register.html'), name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='shop/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)