"""OnlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from home import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page path
    path('', views.home, name='home'),  # Home path
    path('members/', include('django.contrib.auth.urls')),  # Members authentication path
    path('members/', include('members.urls')),  # Members path
    path('store/', include('store.urls')),  # Store path
    # Reset password view ------------------------------------------------
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='members/password_reset.html'),
         name='password_reset'),  # Reset password path
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='members/password_reset_confirm.html'),
         name='password_reset_confirm'),  # Confirm reset password path
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='members/password_reset_done.html'),
         name='password_reset_done'),  # Reset password done path
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='members/password_reset_complete.html'),
         name='password_reset_complete'),  # Reset password complete path
]

# Only use this in development 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
