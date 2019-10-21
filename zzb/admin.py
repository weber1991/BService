from django.contrib import admin
from zzb.models import *
# Register your models here.


@admin.register(zzTime)
class zzTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')
    list_display_links = ['id', 'name']
    list_editable = ['state']

@admin.register(zzBaseComfig)
class zzBaseConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'use')
    list_display_links = ['id', 'name']
    list_editable = ['use']