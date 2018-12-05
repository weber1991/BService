from django.contrib import admin
from wait.models import Screlation
# Register your models here.
class ScrelationAadmin(admin.ModelAdmin):
    list_display = ( 'counterno', 'serviceno', 'servicename', 'serviceid')
    list_editable = ['serviceno', 'servicename', 'serviceid']

    ordering = ("serviceid",)


admin.site.register(Screlation, ScrelationAadmin)