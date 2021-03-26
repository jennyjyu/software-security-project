"""secfit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
import os


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("workouts.urls")),

    # Redirect to login page after reset password.
    path('accounts/login/', RedirectView.as_view(url='https://localhost:'+str(os.environ.get('GROUPID', '90'))+str(os.environ.get('PORTPREFIX', '90'))+'/login.html')),
    path('accounts/', include('django.contrib.auth.urls')),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
