#-*-coding:utf-8-*-
from django.shortcuts import render
from wait.selectWaitingCount import selectWaitingCount
from wait.selectWaitingCountFang import selectWaitingCountFang
from wait.selectWaitingCountNoWork import selectWaitingCountNoWork
import datetime
from wait.UsePymysql0 import dateQuery
# Create your views here.
from wait.models import *



def get_servicelist(temp_str):
    try:
        serviceNoList = temp_str.split(',')
        return serviceNoList
    except:
        return False

def get_ticketList(serviceno):
    '''
        根据业务编号获取当前业务票号序列
    '''
    try:
        ticketList = Ticket.objects.filter(serviceno = int(serviceno), processingstatus=0)
        return ticketList
    except:
        return False

def get_countList():
    # 获取所有窗口关系表
    serviceList = Screlation.objects.all()
    # 等候人数的序列
    '''
    构造的数据：
    1、counterno，窗口号
    2、servicename，业务名称
    3、serviceid，排序号
    4、waitingnumber，等候人数
    5、ticketList，等候人数序列，以printtime为排序依据
    '''
    countList = []


    for service in serviceList:
        temp = {}
        temp['serviceid'] = service.serviceid   # 排序号
        temp['counterno'] = service.counterno   # 获取窗口号
        temp['servicename'] = service.servicename   # 获取业务代号名称

        temp_serviceno = get_servicelist(service.serviceno) # 分解serviceno序列
        # 如果出现错误则默认为0和无
        if temp_serviceno == False:
            temp['waitingnumber'] = 0
            temp['ticket'] = '无'
        else:
            # 针对每个业务进行选择然后叠加
            temp_count = 0
            temp_waitnumberList = []
            temp_ticketList = Ticket.objects.none()
            for serviceno in temp_serviceno:
                # 获取该项业务等候情况的序列
                temp_ticketList_one = get_ticketList(serviceno)
                # 获取每个业务所等待的人数，构造成每个窗口等候人数情况
                temp_count += temp_ticketList_one.count()
                # 将每个业务所等待的情况合并起来，构造成该窗口等候人数的情况
                temp_ticketList = temp_ticketList | temp_ticketList_one
            
            temp['waitingnumber'] = temp_count       
            temp['ticketList'] = temp_ticketList.order_by('printtime') # 按时间排序

        countList.append(temp)
    return countList



def get_workstate():
    '''
    获取当前的工作状态
    dayState：0，1，2--工作日，法定节假日，节假日补休，休息日
    timeState：0，1，工作时间，非工作时间
    '''
    import json,requests,datetime

    # 先判断工作日再判断时间
    ans = {'timeState':0, 'dayState':0}
    now = datetime.datetime.now()
    dayStr = now.strftime("%Y%m%d")

    APIUrl = 'https://api.goseek.cn/Tools/holiday?date='
    api = APIUrl + dayStr
    req = requests.get(api)
    answer = json.loads(req.text)
    req.close()
    ans['dayState'] = answer['data']

    timeStr = int(now.strftime('%H%M'))
    # 工作时间为8：30-12：00，14：00-17：30
    # 可以用时间模块来比较，但这里直接转换为整数来比较，考虑到提前取号，所以整个时间段为800-1730，

    if (timeStr > 800) and (timeStr < 1730):
        ans['timeState'] = 0
    else:
        ans['timeState'] = 1 
    return ans




def index(req):   
    workState = get_workstate()
    #print(workState)
    #if workState['dayState'] != 0:
    #    message = '您好，今天是非工作日，祝您假日愉快。'
    #    return render(req, 'wait/wait_message.html', {'message': message})
    #elif workState['timeState'] != 0:
    #    message = '您好，现在是非工作时间，暂无票号轮候情况。'
    #    return render(req, 'wait/wait_message.html', {'message': message})
    dataList = get_countList()
    return render(req, 'wait/wait_index.html', {'dataList': dataList})
 



   

def wait_test(req):
    # serviceList = Service.objects.all()
    # 获取所有窗口关系表
    serviceList = Screlation.objects.all()
    
    # 获取所有票号
    ticketList = Ticket.objects.all()

    # 等候人数的序列
    '''
    构造的数据：
    1、counterno
    2、serviceno
    3、servicename
    4、serviceid
    5、waitingnumber
    6、ticketno
    '''
    countList = []
    for service in serviceList:
        temp = {}
        temp['servicename'] = service.servicename
        # 分解serviceno序列
        temp_serviceno = get_servicelist(service.serviceno)
        # 如果出现错误则默认为0和无
        if temp_serviceno == False:
            temp['count'] = 0
            temp['waitingnumber'] = '无'
        else:
            # 针对每个业务进行选择然后叠加
            temp_count = 0
            for serviceno in temp_serviceno:
                temp_count += ticketList.filter(serviceno = int(serviceno)).count()
            temp['count'] = temp_count
        # 如何获取下一个办理号码
        countList.append(temp)
    return render(req, 'wait/wait_test.html',{
        'message':'success',
        'countList':countList,
    })