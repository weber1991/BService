from django.conf.urls import url
from dlzp.views import *


app_name = 'dlzp'
urlpatterns = [
    url(r'dlzp_login/$', login, name='login'),
]
