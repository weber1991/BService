from django.shortcuts import render
from wxjz.models import *
from django.db.models import Q

# Create your views here.


def wxjz_index(req):
    return render(req, 'wxjz/wxjz_index.html',)

def index(req):
    sqtype = wxjz_type.objects.filter(name='社区村').first()
    bmtype = wxjz_type.objects.filter(name='部门机构').first()
    othertype = wxjz_type.objects.exclude(name='社区村')
    othertype = othertype.exclude(name='部门机构')

    sqlist = wxjz.objects.filter(type=sqtype)
    bmlist = wxjz.objects.filter(type=bmtype)
    alllist = wxjz.objects.all

    return render(req, 'wxjz/wxjz.html',locals())