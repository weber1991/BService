from django.contrib import admin
from wxjz.models import *
# Register your models here.


class wxjzAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'orderid')
    list_display_links = ['id', 'name']
    list_editable = ['orderid']
    list_filter = ['type']
    search_fields = ['name']

class wxjztypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'orderid')
    list_display_links = ['id', 'name']
    list_editable = ['orderid']


admin.site.register(wxjz_type, wxjztypeAdmin)
admin.site.register(wxjz, wxjzAdmin)
