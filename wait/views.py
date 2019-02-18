#-*-coding:utf-8-*-
from django.shortcuts import render
from wait.selectWaitingCount import selectWaitingCount
from wait.selectWaitingCountFang import selectWaitingCountFang
from wait.selectWaitingCountNoWork import selectWaitingCountNoWork
import datetime
from wait.UsePymysql0 import dateQuery
# Create your views here.
from wait.models import *



def index(req):
    try:
        dateToday = datetime.datetime.now().date().strftime('%Y%m%d')
        dateHour = datetime.datetime.now().hour  # type is int
        # status = dateQuery(dateToday)
        status = '0'
        if status != '0':  # '0' is working , '1'is weekend, '2' is holiday
            print('this is ' + status + '.')
            dataList = {}
            return render(req, 'wait/indexHoliday.html', {'dataList': dataList})
        elif (dateHour <= 22) and (dateHour >= 7):  # working time is 8:00--18:00
            print('this is working.')
            dataList = selectWaitingCount()
            return render(req, 'wait/indexShowData.html', {'dataList': dataList})
        else:
            print('this is no work.')
            dataList = selectWaitingCountNoWork()
            return render(req, 'wait/indexnowork.html', {'dataList': dataList})
    except Exception as e:
        print(e)
        dataList = {}
        return render(req, 'wait/indexError.html', {'dataList':dataList})


def wait_test(req):
    serviceList = Service.objects.all()
    return render(req, 'wait/wait_test.html', {
        'message':'success',
        'serviceList':serviceList,
    })