import pymysql
from django.contrib import admin


pymysql.install_as_MySQLdb()
admin.site.site_header = '后台管理系统'
admin.site.site_title = '后台管理系统'

