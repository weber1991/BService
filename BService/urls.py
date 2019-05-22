"""BService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from BService.settings import MEDIA_ROOT
from django.views.static import serve
from BService.upload import *
from wxjz.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', wxjz_index, name='wxjz_inde'),
    url(r'^wait/', include('wait.urls', namespace='wait')),
    url(r'^dlnews/', include('dlnews.urls', namespace='dlnews')),
    url(r'^zzb/', include('zzb.urls', namespace='zzb')),
    url(r'^wxjz/', include('wxjz.urls', namespace='wxjz')),
    url(r'^dlzp/', include('dlzp.urls', namespace='dlzp')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    url(r'^admin/uploads/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r"^uploads/(?P<path>.*)$", serve, {"document_root": MEDIA_ROOT, }),
    
]
