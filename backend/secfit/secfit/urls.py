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
from django.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from secfit import views


#@login_required
#def protected_serve(request, path, document_root=None, show_indexes=False):
    #return serve(request, path, document_root, show_indexes)
    #return HttpResponse(status=200)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("workouts.urls")),
    re_path(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], views.MediaDetail.as_view(), {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
