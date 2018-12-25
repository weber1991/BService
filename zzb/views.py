from django.shortcuts import render, redirect
from zzb.models import *
import os
from django.conf import settings
from django.core import paginator
import datetime
from django.http import HttpResponse, FileResponse
from xlwt import *
import xlrd
import io

# Create your views here.

PAGECOUNT = 50


'''
在模板中使用session：{{ request.session.username }}
是request而不是req
'''


def get_age(chusheng):
    try:
        chusheng = datetime.datetime.strptime(chusheng, '%Y-%m-%d')
        today = datetime.datetime.today()
        count = today - chusheng
        age = int(count/365)
        return age
    except:
        return ''

def zzb_temp(req):
    return render(req, 'zzb/zzb_temp.html',{'title': '告示','content':'功能未开放，敬请期待。'})

def index(req):
    zztime = zzTime.objects.get(id=1)
    if zztime:
        now = datetime.datetime.now()
        if now > zztime.startbm:
            # session
            username = req.session.get('username', None)
            if username:
                user = zzUser.objects.get(idcard=username)
                return render(req, 'zzb/index.html', {'user': user})
            else:
                return redirect('zzb:login')
        else:
            answer = '未到开放报名时间'
            return render(req, 'zzb/time_out.html', {'zztime': zztime, 'answer': answer})
    else:
        answer = '系统维护中'
        return render(req, 'zzb/time_out.html', {'zzbtime':None, 'answer':answer})


def superme(req):
    # session
    username = req.session.get('username', None)
    if username:
        user = zzUser.objects.get(idcard=username)
        return render(req, 'zzb/index.html', {'user': user})
    else:
        return redirect('zzb:login')


def login(req):
    if req.method == 'GET':
        return render(req, 'zzb/login.html', {})
    else:
        username = req.POST.get('username', None)

        password = req.POST.get('password', None)
        print(username, password)
        user = zzUser.objects.filter(idcard = username, password=password)
        if len(user) == 0:
            return redirect('zzb:login')
        else:
            req.session['username'] = username
            print(req.session['username'])
            return redirect('zzb:index')


def register(req):
    if req.method == 'GET':
        return render(req, 'zzb/login.html', {})
    else:
        username = req.POST.get('username', None)
        idcard = req.POST.get('idcard', None)
        password1 = req.POST.get('password1', '111111')
        password2 = req.POST.get('password2', '123456')
        print(username,idcard,password1,password2)
        if (password1 == password2) and username and idcard:
            count = zzUser.objects.filter(idcard=idcard)
            if len(count) == 0:
                user = zzUser.objects.create(username = username, password= password1,idcard=idcard, logo='')
                answer = '账号注册成功'
                return render(req, 'zzb/regist_answer.html', {'answer':answer})
            else:
                answer = '账号已被注册'
                return render(req, 'zzb/regist_answer.html', {'answer': answer})
        else:
            answer = '密码不同'
            return render(req, 'zzb/regist_answer.html', {'answer': answer})


def logout(req):
    del req.session["username"]
    return redirect('zzb:login')


def reset_password(req):
    name = req.POST.get('name', None)
    idcard = req.POST.get('idcard',None)

    userlist = zzUser.objects.filter(username=name, idcard=idcard)
    if len(userlist) == 0:
        answer = '重置密码失败'
        return render(req, 'zzb/regist_answer.html', {'answer': answer})
    else:
        user = userlist.first()
        user.password = "111111"
        user.save()
        answer = '重置成功，密码为111111，请回到登陆界面登陆。'
        return render(req, 'zzb/regist_answer.html', {'answer': answer})


def set_password(req):
    try:
        username = req.session.get('username', None)
    except:
        return redirect('zzb:login')
    if username is None:
        return redirect('zzb:login')
    user = zzUser.objects.get(idcard=username)

    if req.method == 'GET':
        return render(req, 'zzb/set_password.html', {'user':user})
    else:
        password1 = req.POST.get('password1', None)
        password2 = req.POST.get('password2', None)
        if password1 and password2 and (password1==password2):
            user.password = password2
            user.save()
            title = '修改成功'
            content = '修改成功。请妥善保管密码。'
            return render(req, 'zzb/zzb_temp.html', {'title': title, 'content': content})
        else:
            title = '修改失败'
            content = '修改失败。请保证两次输入密码相同。'
            return render(req, 'zzb/zzb_temp.html', {'title': title, 'content': content})



def notice_list(req):
    pageDict = {}
    pageDict["allCount"] = zzNotice.objects.filter(state='发布').count()
    pageDict["allPage"] = int(pageDict["allCount"] / PAGECOUNT)
    if (pageDict["allCount"] % PAGECOUNT) != 0:
        pageDict["allPage"] += 1
    try:
        pageDict["nowPage"] = int(req.GET.get("nowPage", 1))
        pageDict["pageType"] = req.GET.get("pageType",'')
    except:
        pass
    if pageDict["pageType"] == 'next':
        pageDict["nowPage"] += 1
    elif pageDict["pageType"] == 'last':
        pageDict["nowPage"] -= 1

    noticelist = zzNotice.objects.filter(state='发布').order_by('-date_publish')[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]
    return render(req, 'zzb/notice_list.html',
                  {'noticelist':noticelist,
                   'pageDict':pageDict})


def notice_list_all(req):
    pageDict = {}
    pageDict["allCount"] = zzNotice.objects.count()
    pageDict["allPage"] = int(pageDict["allCount"] / PAGECOUNT)
    if (pageDict["allCount"] % PAGECOUNT) != 0:
        pageDict["allPage"] += 1
    try:
        pageDict["nowPage"] = int(req.GET.get("nowPage", 1))
        pageDict["pageType"] = req.GET.get("pageType",'')
    except:
        pass
    if pageDict["pageType"] == 'next':
        pageDict["nowPage"] += 1
    elif pageDict["pageType"] == 'last':
        pageDict["nowPage"] -= 1

    noticelistall = zzNotice.objects.all().order_by('-date_publish')[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]
    return render(req, 'zzb/notice_list_all.html',
                  {'noticelistall':noticelistall,
                   'pageDict':pageDict})


def notice_add(req):
    '''
    session传递有点问题，需要再做研究
    :param req:
    :return:
    '''
    # user = req.session.get('username',None)
    # print('notice_add:'+user)
    if req.method == 'GET':
        #if user:
        #   return redirect('zzb:login')
        return render(req, 'zzb/notice_add.html',{})
    else:
        title = req.POST.get('title', None)
        user = req.POST.get('user', None)
        content = req.POST.get('content', None)
        if title and user and content:
            notice = zzNotice.objects.create(title=title, user = user, content=content, state = '草稿')
            return redirect('zzb:notice_list_all')
        else:
            return redirect('zzb:notice_add')

def notice_editor(req, id):
    notice = zzNotice.objects.get(id=id)
    if req.method == 'GET':
        return render(req, 'zzb/notice_editor.html',{'notice':notice})
    else:
        title = req.POST.get('title', None)
        user = req.POST.get('user', None)
        content = req.POST.get('content', None)
        if title and user and content:
            notice.title = title
            notice.user = user
            notice.content = content
            notice.state = '草稿'
            notice.save()
            return redirect('zzb:notice_list_all')
        return render('zzb:notice_editor', id)

def notice_look(req, id):
    notice = zzNotice.objects.get(id = id)
    return render(req, 'zzb/notice_look.html', {'notice':notice})

def notice_change(req, id):
    notice = zzNotice.objects.get(id = id)
    if notice.state == '草稿':
        notice.state = '发布'
    else:
        notice.state = '草稿'
    notice.save()
    return redirect('zzb:notice_list_all')


def notice_delete(req, id):
    notice = zzNotice.objects.get(id = id)
    notice.delete()
    return redirect('zzb:notice_list_all')

# 岗位新增
def job_add(req):
    if req.method == 'GET':
        return render(req, 'zzb/job_add.html', {})
    else:
        name = req.POST.get('name', None)
        daihao = req.POST.get('daihao', None)
        count = req.POST.get('count', None)
        education = req.POST.get('education', None)
        major = req.POST.get('major', None)
        other = req.POST.get('other', None)
        note = req.POST.get('note', ' ')
        hold0 = req.POST.get('hold0', None)
        if name and daihao and count and education and major and other:
            job = zzJob.objects.create(name=name,
                                       daihao=daihao,
                                       count=count,
                                       education=education,
                                       major=major,
                                       other=other,
                                       note=note,
                                       # hold0=hold0,
                                       state='草稿')
        else:
            return redirect('zzb:job_add')
        return redirect('zzb:job_list_all')

# 岗位编辑
def job_editor(req, id):
    job = zzJob.objects.get(id = id)
    if req.method == 'GET':
        return render(req, 'zzb/job_editor.html',{'job': job})
    elif req.method == 'POST':
        job.name = req.POST.get('name', None)
        job.daihao = req.POST.get('daihao', None)
        job.count = req.POST.get('count', None)
        job.education = req.POST.get('education', None)
        job.major = req.POST.get('major', None)
        job.other = req.POST.get('other', None)
        job.note = req.POST.get('note', None)
        # job.hold0 = req.POST.get('hold0', None)
        job.state = '草稿'
        job.save()
        return redirect('zzb:job_list_all')


def job_delete(req, id):
    job = zzJob.objects.get(id=id)
    job.delete()
    return redirect('zzb:job_list_all')

def job_data(req, id):
    job = zzJob.objects.get(id = id)
    return render(req, 'zzb/job_data.html', {'job':job})

# 岗位查询-对外-对个人
def job_list(req):
    joblist = zzJob.objects.filter(state='发布')
    return render(req, 'zzb/job_list.html',{'joblist':joblist})

# 岗位查询-对内
def job_list_all(req):
    joblistall = zzJob.objects.all()
    return render(req, 'zzb/job_list_all.html', {'joblistall': joblistall})

# 岗位发布-草稿变发布
def job_change(req, id):
    job = zzJob.objects.get(id = id)
    if job.state == '草稿':
        job.state = '发布'
    else:
        job.state = '草稿'
    job.save()
    return redirect('zzb:job_list_all')

# 报名
def join_job(req):
    username = req.session.get('username', None)
    user = zzUser.objects.get(idcard=username)
    zztime = zzTime.objects.get(id=1)
    if zztime:
        now = datetime.datetime.now()
        if now > zztime.endbm:
            title = '已经结束报名。'
            content = '报名截止时间为：' + str(zztime.endbm)
            return render(req, 'zzb/zzb_temp.html', {'title':title, 'content': content})
    if username:
        userextendlist = zzUserExtend.objects.filter(user=user)
        # 判断有没有填写资料，没有则跳转
        if len(userextendlist) == 0:
            return redirect('zzb:mydata')
        if userextendlist[0].jiguan is '' and userextendlist[0].phone is '':
            # message = "您的信息并不完善，请先个人信息中填写完整"
            return redirect('zzb:mydata')
        if req.method == 'GET':
            userextend = userextendlist.first()
            joinjoblist = zzJoinJob.objects.filter(user=userextend)
            if len(joinjoblist) == 0:
                # 未报名
                # myjoblist = zzJob.objects.filter(state='发布')
                # 这里添加条件筛选
                # 年龄过虑
                myjoblist = []
                joblist = zzJob.objects.filter(state='发布')
                try:
                    # 年龄过滤
                    # mydate = datetime.datetime.strptime(userextend.chusheng, "%Y-%m-%d")
                    # for job in joblist:
                    #     jobdate = datetime.datetime.strptime(job.hold0, "%Y-%m-%d")
                    #     if mydate >= jobdate:
                    #         myjoblist.append(job)
                    # 年龄不过滤
                    myjoblist = joblist
                    return render(req, 'zzb/join_job.html', {'joblist': myjoblist, 'userextend': userextend})
                except:
                    title = '无法获取报名信息'
                    content = '请正确填写个人资料。'
                    return render(req, 'zzb/zzb_temp.html', {'title': title, 'content': content})
            # 如果已经报名的话
            #return redirect('zzb:join_list')
            return render(req, 'zzb/join_job_suceess.html', {})
        else:
            jobid = req.POST.get('job', None)
            if jobid:
                job = zzJob.objects.get(id = jobid)
                joinjob = zzJoinJob.objects.create(job=job, user=userextendlist.first(), state='已提交报名', sweat='')
                # return redirect('zzb:join_list')
                return render(req, 'zzb/join_job_suceess.html', {})
            else:
                return redirect('zzb:join_list')
    else:
        return  redirect('zzb:login')

def join_list(req):
    username = req.session.get('username', None)
    user = zzUser.objects.get(idcard=username)
    userextend = zzUserExtend.objects.filter(user = user).first()
    joinlist = zzJoinJob.objects.filter(user=userextend)
    if len(joinlist) == 0:
        content = '抱歉，没有您的考试报名信息，请先报名考试。'
        return render(req, 'zzb/zzb_temp.html', {'content':content})
    else:
        joinjob = joinlist.first()
        return render(req, 'zzb/join_list.html', {'joinjob':joinjob, 'userextend':userextend})

def join_show(req, id):
    joinjob = zzJoinJob.objects.get(id = id)
    userextend = joinjob.user
    return render(req, 'zzb/join_show.html', {'joinjob':joinjob, 'userextend':userextend})

def join_list_all(req):
    pageDict = {}
    pageDict["allCount"] = zzJoinJob.objects.count()
    pageDict["allPage"] = int(pageDict["allCount"] / PAGECOUNT)
    if (pageDict["allCount"] % PAGECOUNT) != 0:
        pageDict["allPage"] += 1
    try:
        pageDict["nowPage"] = int(req.GET.get("nowPage", 1))
        pageDict["pageType"] = req.GET.get("pageType",'')
    except:
        pass
    if pageDict["pageType"] == 'next':
        pageDict["nowPage"] += 1
    elif pageDict["pageType"] == 'last':
        pageDict["nowPage"] -= 1

    firstCount = (pageDict["nowPage"]-1)*PAGECOUNT

    joinjoblistall = zzJoinJob.objects.all()[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]
    return render(req, 'zzb/join_list_all.html', {'joinjoblistall': joinjoblistall,
                                                  'pageDict':pageDict,
                                                  'firstCount':firstCount})

def join_success(req, id):
    joinjob = zzJoinJob.objects.get(id = id)
    joinjob.state = '审核通过'
    joinjob.save()
    return redirect('zzb:join_list_all')

def join_faile(req, id):
    joinjob = zzJoinJob.objects.get(id = id)
    joinjob.state = '待审核'
    joinjob.save()
    return redirect('zzb:join_list_all')

def join_count(req):
    # 构造序列
    # 每个岗位分别对应的报考人数有多少，报考人员的序列

    countlist = []
    joblist = zzJob.objects.filter(state = '发布')
    joinjoblist = zzJoinJob.objects.all()

    for job in joblist:
        count = {}
        joinlist = joinjoblist.filter(job=job)
        count["number"] = len(joinlist)
        if count["number"] > 0:
            count["joinlist"] = joinlist
        else:
            count["joinlist"] = False
        count["job"] = job
        countlist.append(count)

    return render(req, 'zzb/join_count.html', {'countlist':countlist})

def join_job_count(req, id):
    job = zzJob.objects.get(id = id)
    joinjoblist = zzJoinJob.objects.filter(job=job)
    return render(req, 'zzb/join_job_count.html', {'joinjoblist':joinjoblist})

# 打印报名表
def print_joinjob(req, id):
    # session
    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')

    user = zzUser.objects.get(idcard=username)
    userextendlist = zzUserExtend.objects.filter(user=user)

    # 注意：get方法如果获取不到数据会直接报错
    try:
        joinjob = zzJoinJob.objects.get(id = id)
    except:
        return render(req, 'zzb/zzb_bmb.html', {})

    userextend = userextendlist.first()
    if joinjob.user == userextend:
        return render(req, 'zzb/zzb_bmb.html',{'joinjob':joinjob})
    if user.power > 0:
        return render(req, 'zzb/zzb_bmb.html', {'joinjob':joinjob})
    return render(req, 'zzb/zzb_bmb.html', {})


# 座位生成
def seat_create(req):
    import random
    # 输入科室数，每个科室座位数，输入所有考生的序列
    # 最终结果以第一科室第一座位开始排列，再获取考生序列，打乱，再一一分配过去
    # 最终序列效果：{"科室号"：1,2,3....,{"座位"}：{}}

    # 7月9日更新需要：需要按照各个岗位来进行排位，相同岗位坐埋一起。
    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')


    joinjoblist = zzJoinJob.objects.all()
    if req.method == 'GET':
        return render(req, 'zzb/seat_create.html', {'joinjobcount':len(joinjoblist)})
    else:
        # 在表单里面验证，而不在后台做
        # 验证数量合不合格
        # 验证输入是否为数字
        class_count = int(req.POST.get('met_class', None))
        seat_count = int(req.POST.get('met_seat', None))
        joblist = zzJob.objects.filter(state='发布')

        # 构造座位号序列
        seatlist = []
        for i in range(1, class_count+1):
            class_no = str(i).zfill(2)
            for j in range(1, seat_count+1):
                seat_no = str(j).zfill(2)
                seat = class_no + '-'+ seat_no
                seatlist.append(seat)
        print(seatlist)

        seat_index = 0
        for job in joblist:
            joinlist = joinjoblist.filter(job=job)
            joinindexlist = []
            jobnumber = job.daihao.replace('PY', '').replace('ZA', '')

            for i in range(0, len(joinlist)):
                joinindexlist.append(i)
            random.shuffle(joinindexlist)
            random.shuffle(joinindexlist)

            indexcount = 1
            year = str(datetime.datetime.now().year)
            for i in joinindexlist:
                joinlist[i].sweat = seatlist[seat_index]
                joinlist[i].process = '打印准考证'
                # joinlist[i].zkzh = year + jobnumber + str(indexcount).zfill(3)
                joinlist[i].zkzh = year + jobnumber + str(indexcount).zfill(4)
                joinlist[i].save()
                seat_index += 1
                indexcount += 1
        try:
            joinjoblist = joinjoblist.order_by("sweat")
        except:
            pass
        return render(req, 'zzb/seat_list.html', {'joinjoblist':joinjoblist})


def seat_list(req):
    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')
    pageDict = {}
    pageDict["allCount"] = zzJoinJob.objects.count()
    pageDict["allPage"] = int(pageDict["allCount"] / PAGECOUNT)
    if (pageDict["allCount"] % PAGECOUNT) != 0:
        pageDict["allPage"] += 1
    try:
        pageDict["nowPage"] = int(req.GET.get("nowPage", 1))
        pageDict["pageType"] = req.GET.get("pageType", '')
    except:
        pass
    if pageDict["pageType"] == 'next':
        pageDict["nowPage"] += 1
    elif pageDict["pageType"] == 'last':
        pageDict["nowPage"] -= 1

    try:
        joinjoblist = zzJoinJob.objects.all().order_by("sweat")[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]
    except:
        joinjoblist = zzJoinJob.objects.all()[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]

    return render(req, 'zzb/seat_list.html',
                  {'joinjoblist': joinjoblist,
                   'pageDict':pageDict})


def paper_list(req):
    zztime = zzTime.objects.get(id=1)
    if zztime:
        now = datetime.datetime.now()
        if now < zztime.startdy:
            title = '未到打印时间'
            content = '开放打印时间为'+ str(zztime.startdy)
            return render(req, 'zzb/zzb_temp.html', {'title':title, 'content':content})
    # session
        if now > zztime.enddy:
            title = '已超过打印时间'
            content = '打印准考证最迟时间为' + str(zztime.enddy)
            return render(req, 'zzb/zzb_temp.html', {'title': title, 'content': content})

    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')

    user = zzUser.objects.get(idcard=username)
    userextendlist = zzUserExtend.objects.filter(user=user)
    joinjoblist = zzJoinJob.objects.filter(user=userextendlist.first())
    if len(joinjoblist) == 0:
        return redirect('zzb:join_job')
    joinjob = joinjoblist.first()
    return render(req, 'zzb/paper_list.html', {'joinjob': joinjob})



def paper_list_all(req):
    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')

    pageDict = {}
    pageDict["allCount"] = zzJoinJob.objects.count()
    pageDict["allPage"] = int(pageDict["allCount"] / PAGECOUNT)
    if (pageDict["allCount"] % PAGECOUNT) != 0:
        pageDict["allPage"] += 1
    try:
        pageDict["nowPage"] = int(req.GET.get("nowPage", 1))
        pageDict["pageType"] = req.GET.get("pageType", '')
    except:
        pass
    if pageDict["pageType"] == 'next':
        pageDict["nowPage"] += 1
    elif pageDict["pageType"] == 'last':
        pageDict["nowPage"] -= 1

    try:
        joinjoblist = zzJoinJob.objects.all().order_by("sweat")[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]
    except:
        joinjoblist = zzJoinJob.objects.all()[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]
    return render(req, 'zzb/paper_list_all.html',
                  {'joinjoblist':joinjoblist,
                   'pageDict':pageDict})

def paper_data(req, id):
    joinjob = zzJoinJob.objects.get(id = id)
    zztime = zzTime.objects.get(id=1)

    return render(req, 'zzb/paper_list.html', {'joinjob':joinjob})

def print_zkz(req, id):
    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')

    user = zzUser.objects.get(idcard=username)
    userextendlist = zzUserExtend.objects.filter(user=user)

    # 注意：get方法如果获取不到数据会直接报错
    try:
        joinjob = zzJoinJob.objects.get(id = id)
    except:
        return render(req, 'zzb/zzb_zkz.html', {})

    userextend = userextendlist.first()
    if joinjob.user == userextend:
        return render(req, 'zzb/zzb_zkz.html',{'joinjob':joinjob})
    if user.power > 0:
        return render(req, 'zzb/zzb_zkz.html', {'joinjob':joinjob})
    return render(req, 'zzb/zzb_zkz.html', {})

def joinjob_excel(req):
    joinjoblist = zzJoinJob.objects.all()
    if joinjoblist:
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet('第一页')
        w.write(0, 0, '序号')
        w.write(0, 1, '岗位')
        w.write(0, 2, '姓名')
        w.write(0, 3, '性别')
        w.write(0, 4, '身份证号码')
        w.write(0, 5, '出生年月')
        w.write(0, 6, '年龄')
        w.write(0, 7, '准考证号')
        w.write(0, 8, '试室号')
        w.write(0, 9, '座位号')
        w.write(0, 10, '笔试成绩')
        w.write(0, 11, '面试成绩')
        w.write(0, 12, '笔试面试合成成绩（笔试占40%，面试占60%）')
        w.write(0, 13, '政治面貌')
        w.write(0, 14, '籍贯')
        w.write(0, 15, '户口所在地')
        w.write(0, 16, '毕业院校')
        w.write(0, 17, '专业')
        w.write(0, 18, '学历（学位）')
        w.write(0, 19, '毕业时间')
        w.write(0, 20, '工作单位及职务')
        w.write(0, 21, '职称')
        w.write(0, 22, '联系电话')
        w.write(0, 23, '备注')
        excel_row = 1
        for joinjob in joinjoblist:
            exl_name = joinjob.user.name
            exl_daihao = joinjob.job.daihao
            exl_sex = joinjob.user.sex
            exl_idcard = joinjob.user.idcard
            exl_chusheng = joinjob.user.chusheng
            exl_age = get_age(exl_chusheng)
            exl_zkzh = joinjob.zkzh.replace('-', '')
            exl_class = get_class(joinjob.sweat)
            exl_seat = get_seat(joinjob.sweat)
            # 笔试
            # 面试
            # 综合成绩
            exl_mianmao = joinjob.user.mianmao
            exl_jiguan = joinjob.user.jiguan
            exl_hukou = joinjob.user.huji
            exl_xuexiao = joinjob.user.xuexiao
            exl_zhuanye = joinjob.user.zhuanye
            exl_xueli = joinjob.user.xueli
            exl_biye = joinjob.user.biye
            exl_danwei = joinjob.user.danwei
            exl_zhicheng = joinjob.user.zhiye1
            exl_phone = joinjob.user.phone
            exl_beizhu = joinjob.user.beizhu

            w.write(excel_row, 0, str(excel_row))
            w.write(excel_row, 1, exl_daihao)
            w.write(excel_row, 2, exl_name)
            w.write(excel_row, 3, exl_sex)
            w.write(excel_row, 4, exl_idcard)
            w.write(excel_row, 5, exl_chusheng)
            w.write(excel_row, 6, exl_age) # 年龄
            w.write(excel_row, 7, exl_zkzh)
            w.write(excel_row, 8, exl_class)
            w.write(excel_row, 9, exl_seat)
            # w.write(excel_row, 10, ) # 笔试
            # w.write(excel_row, 11, ) # 面试
            # w.write(excel_row, 12, ) # 综合
            w.write(excel_row, 13, exl_mianmao)
            w.write(excel_row, 14, exl_jiguan)
            w.write(excel_row, 15, exl_hukou)
            w.write(excel_row, 16, exl_xuexiao)
            w.write(excel_row, 17, exl_zhuanye)
            w.write(excel_row, 18, exl_xueli)
            w.write(excel_row, 19, exl_biye)
            w.write(excel_row, 20, exl_danwei)
            w.write(excel_row, 21, exl_zhicheng)
            w.write(excel_row, 22, exl_phone)
            w.write(excel_row, 23, exl_beizhu)
            excel_row += 1

        excel_path = "media\\zzb\\joinjoblist.xls"
        exist_file = os.path.exists(excel_path)
        if exist_file:
            os.remove(os.path.join(settings.BASE_DIR, excel_path))
        ws.save(os.path.join(settings.BASE_DIR, excel_path))
        import BService.settings
        file = open(os.path.join(settings.BASE_DIR, excel_path),'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="joinjoblist.xls"'
        return response

def seat_excel(req):
    joinjoblist = zzJoinJob.objects.all().order_by('sweat')
    class_count = int(len(joinjoblist)/30) + 1
    class_count_index = 1
    ws = Workbook(encoding='utf-8')
    for ws_i in range(0, class_count):
        # 每一页
        sheet_name = '第' + str(class_count_index) + '试室'
        w = ws.add_sheet(sheet_name)
        w.write_merge(0, 0, 0, 6, sheet_name)
        w.write(2, 0, '序号')
        w.write(2, 1, '姓名')
        w.write(2, 2, '性别')
        w.write(2, 3, '准考证号')
        w.write(2, 4, '试室号')
        w.write(2, 5, '座位号')
        excel_row = 3
        # 每页内容
        joinjoblist_start = (class_count_index-1) * 30
        joinjoblist_end = (class_count_index - 1) * 30 + 30
        if joinjoblist_start > len(joinjoblist):
            joinjoblist_start = len(joinjoblist)

        if joinjoblist_end > len(joinjoblist):
            joinjoblist_end = len(joinjoblist)
        class_count_index += 1
        for joinjob in joinjoblist[joinjoblist_start:joinjoblist_end]:
            exl_name = joinjob.user.name
            exl_sex = joinjob.user.sex
            exl_zkzh = joinjob.zkzh.replace('-', '')
            exl_class = get_class(joinjob.sweat)
            exl_seat = get_seat(joinjob.sweat)
            w.write(excel_row, 0, excel_row-2)
            w.write(excel_row, 1, exl_name)
            w.write(excel_row, 2, exl_sex)
            w.write(excel_row, 3, exl_zkzh)
            w.write(excel_row, 4, exl_class)
            w.write(excel_row, 5, exl_seat)
            excel_row += 1

    excel_path = "media\\zzb\\classlist.xls"
    exist_file = os.path.exists(excel_path)
    if exist_file:
        os.remove(os.path.join(settings.BASE_DIR, excel_path))
    ws.save(os.path.join(settings.BASE_DIR, excel_path))

    import BService.settings
    file = open(os.path.join(settings.BASE_DIR, excel_path),'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="classlist.xls"'
    return response

def seat_data_excel(req):
    joinjoblist = zzJoinJob.objects.all().order_by('sweat')
    class_count = int(len(joinjoblist)/30) + 1 # 试室数
    class_count_index = 1
    ws = Workbook(encoding='utf-8')
    for ws_i in range(0, class_count):
        # 每一页
        sheet_name = '第' + str(class_count_index) + '试室'
        w = ws.add_sheet(sheet_name)
        # 每页内容
        joinjoblist_start = (class_count_index-1) * 30
        joinjoblist_end = (class_count_index - 1) * 30 + 30
        if joinjoblist_start > len(joinjoblist):
            joinjoblist_start = len(joinjoblist)
        if joinjoblist_end > len(joinjoblist):
            joinjoblist_end = len(joinjoblist)

        seat_index = 0
        seat_data_row = 0
        seat_data_col = 0
        class_count_index += 1
        for joinjob in joinjoblist[joinjoblist_start:joinjoblist_end]:
            exl_name = '姓    名：'+ joinjob.user.name
            exl_zkzh = '准考证号：'+joinjob.zkzh.replace('-', '')
            exl_idcard = '身份证号：'+joinjob.user.idcard
            exl_class = '试 室 号：第'+str(get_class(joinjob.sweat)) + '试室'
            exl_seat = '座 位 号：'+str(get_seat(joinjob.sweat))

            last_content = exl_name + '\r\n' + exl_zkzh + '\r\n' + exl_idcard + '\r\n' + exl_class + '\r\n' + exl_seat
            w.write(seat_data_row, seat_data_col, last_content)
            seat_index += 1
            seat_data_row = int((seat_index)/4)
            seat_data_col = (seat_index)%4

    excel_path = "media\\zzb\\seatdatalist.xls"
    exist_file = os.path.exists(excel_path)
    if exist_file:
        os.remove(os.path.join(settings.BASE_DIR, excel_path))
    ws.save(os.path.join(settings.BASE_DIR, excel_path))

    import BService.settings
    file = open(os.path.join(settings.BASE_DIR, excel_path),'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="seatdatalist.xls"'
    return response

def get_class(value):
    try:
        value = str(value)
        strlist = value.split('-')
        #return '第%s科室' % (strlist[0])
        return int(strlist[0])
    except:
        return ''

def get_seat(value):
    try:
        value = str(value)
        strlist = value.split('-')
        return int(strlist[1])
    except:
        return ''

def chengji_list(req):
    # 前台判断上传文件类型，确定excle
    # 后台判断并且做数据处理
    pageDict = {}
    pageDict["allCount"] = zzJoinJob.objects.count()
    pageDict["allPage"] = int(pageDict["allCount"] / PAGECOUNT)
    if (pageDict["allCount"] % PAGECOUNT) != 0:
        pageDict["allPage"] += 1
    try:
        pageDict["nowPage"] = int(req.GET.get("nowPage", 1))
        pageDict["pageType"] = req.GET.get("pageType", '')
    except:
        pass
    if pageDict["pageType"] == 'next':
        pageDict["nowPage"] += 1
    elif pageDict["pageType"] == 'last':
        pageDict["nowPage"] -= 1

    joinjoblist = zzJoinJob.objects.all()[(pageDict["nowPage"]-1)*PAGECOUNT:pageDict["nowPage"]*PAGECOUNT]

    if req.method == 'GET':
        # tempJoinJobList = zzJoinJob.objects.all()
        # for i in tempJoinJobList:
        #     zkzh = i.zkzh[0:4]+i.zkzh[6:]
        #     i.zkzh = zkzh
        #     i.save()
        return render(req, 'zzb/chengji_list.html',
                      {'joinjoblist':joinjoblist,'pageDict':pageDict})
    else:
        chengji_file = req.FILES.get('chengji_file', None)
        if chengji_file:
            try:
                data = xlrd.open_workbook(filename=None, file_contents=chengji_file.read())# 关键位置
                table = data.sheet_by_index(0)
                max_row = table.nrows
                max_col = table.ncols
                print(max_row, max_col)
                for i in range(0, max_row):
                    # state用来代表是否进入面试，是或者否---对应第5列
                    # process为是否进入面试----无
                    # score用来表示成绩----对应第3列
                    # note来代表名次-----对应第4列
                    # 唯一标识号，zkzh--对应第2列
                    try:
                        zkzh = int(table.cell(rowx=i, colx=2).value) # 就是excel里面的第三列
                        print(zkzh)
                        joinjob = zzJoinJob.objects.get(zkzh=zkzh)
                        try:
                            state = table.cell(rowx=i, colx=5).value
                        except:
                            state = '待审核'
                        process = '是否进入面试'
                        score = table.cell(rowx=i, colx=3).value
                        try:
                            note = int(table.cell(rowx=i, colx=4).value)
                        except:
                            note = table.cell(rowx=i, colx=4).value
                        joinjob.state = state
                        joinjob.process = process
                        joinjob.score = score
                        joinjob.note = note
                        joinjob.save()
                    except:
                        continue
                return render(req, 'zzb/chengji_list.html', {'joinjoblist':joinjoblist})
            except:
                return render(req, 'zzb/chengji_list.html', {})
        return render(req, 'zzb/chengji_list.html', {})

# 供后台管理员查看，调用同个模板
def chengji_look(req, id):
    joinjob = zzJoinJob.objects.get(id = id)
    return render(req, 'zzb/chengji_data.html', {'joinjob':joinjob})

def chengji_data(req):
    zztime = zzTime.objects.get(id=1)
    if zztime:
        now = datetime.datetime.now()
        if now < zztime.startcj:
            title = '未到查询成绩时间'
            content = '查询成绩时间为' + str(zztime.startcj)
            return render(req, 'zzb/zzb_temp.html', {'title': title, 'content': content})
        # session
        if now > zztime.endcj:
            title = '已超过查询成绩时间'
            content = '查询成绩最迟时间为' + str(zztime.endcj)
            return render(req, 'zzb/zzb_temp.html', {'title': title, 'content': content})

    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')

    user = zzUser.objects.get(idcard=username)
    userextendlist = zzUserExtend.objects.filter(user=user)
    joinjoblist = zzJoinJob.objects.filter(user=userextendlist.first())
    if len(joinjoblist) == 0:
        title = '查询失败'
        content = '查询失败，请确认是否参加考试或联系管理员。'
    joinjob = joinjoblist.first()
    return render(req, 'zzb/chengji_data.html', {'joinjob':joinjob})

# 填写个人资料
def mydata(req):
    import time, random
    username = req.session.get('username', None)
    if username is None:
        return redirect('zzb:login')
    print(username)
    user = zzUser.objects.get(idcard=username)
    userextendlist = zzUserExtend.objects.filter(user=user)
    joinjob = zzJoinJob.objects.filter(user=userextendlist.first())
    if len(joinjob) != 0:
        return render(req, 'zzb/zzb_temp.html', {'title': '告示','content':'您已提交报名，无法修改资料'})
    if req.method == 'GET':
        # 对群众而言，身份证就是登陆账号

        if len(userextendlist) == 0:
            userextend = zzUserExtend.objects.create(user=user, idcard=user.idcard) # ,name=user.name)
            return render(req, 'zzb/mydata.html', {'userextend': userextend })
        userextend = userextendlist.first()
        return render(req, 'zzb/mydata.html', {'userextend':userextend})
    else:
        logo = req.FILES.get('logo',None)
        if logo:
            try:
                fn = time.strftime('%Y%m%d%H%M%S')
                fn = fn + '_%d' % random.randint(0, 100)
                path = 'zzb/' + fn
                path = path + logo.name
                f = open(os.path.join(settings.MEDIA_ROOT, path), 'wb')
                for chunk in logo.chunks(chunk_size=1024):
                    f.write(chunk)
                logourl = '/media/' + path
                print(logourl)
                f.close()
            except Exception as e:
                pass
        else:
            logourl = None
        name = req.POST.get('name', ' ')
        sex = req.POST.get('sex', ' ')
        minzu = req.POST.get('minzu', ' ')
        chusheng = req.POST.get('chusheng', ' ')
        jiguan = req.POST.get('jiguan', ' ')
        mianmao = req.POST.get('mianmao', ' ')
        huji = req.POST.get('huji', ' ')
        note1 = req.POST.get('shequ', ' ')
        hunyin = req.POST.get('hunyin', ' ')
        idcard = req.POST.get('idcard', ' ')
        dianhua = req.POST.get('dianhua', ' ')
        tongxun = req.POST.get('tongxun', ' ')
        youbian = req.POST.get('youbian', ' ')
        xuexiao = req.POST.get('xuexiao', ' ')
        biye = req.POST.get('biye', ' ')
        zhuanye = req.POST.get('zhuanye', ' ')
        xueli = req.POST.get('xueli', ' ')
        waiyu = req.POST.get('waiyu', ' ')
        jisuanji = req.POST.get('jisuanji', ' ')
        danwei = req.POST.get('danwei', ' ')
        xingzhi = req.POST.get('xingzhi', ' ')
        luoshi = req.POST.get('luoshi', ' ')
        jiaozheng = req.POST.get('jiaozheng', ' ')
        shengao = req.POST.get('shengao', ' ')
        jishu = req.POST.get('jishu', ' ')
        zhiye1 = req.POST.get('zhiye1', ' ')
        zhiye2 = req.POST.get('zhiye2', ' ')
        daxue = req.POST.get('daxue', ' ')
        jingli = req.POST.get('jingli', ' ')
        guanxi = req.POST.get('guanxi', '')
        techang = req.POST.get('techang', '')
        jiangfa = req.POST.get('jiangfa', '')
        shenhe = req.POST.get('shenhe', '')
        beizhu = req.POST.get('beizhu', ' ')

        if len(userextendlist) == 0:
            user.logo = 'media/zzb/default.png'
            user.save()
            userextend = zzUserExtend.objects.create(
                user = user,
                name = name,
                sex = sex,
                minzu = minzu,
                chusheng = chusheng,
                jiguan = jiguan,
                mianmao = mianmao,
                huji = huji,
                note1 = note1,
                hunyin = hunyin,
                idcard = idcard,
                phone = dianhua,
                tongxun = tongxun,
                youbian = youbian,
                xuexiao = xuexiao,
                biye = biye,
                zhuanye = zhuanye,
                xueli = xueli,
                waiyu = waiyu,
                jisuanji = jisuanji,
                danwei = danwei,
                xingzhi = xingzhi,
                luoshi = luoshi,
                jiaozheng = jiaozheng,
                shengao = shengao,
                jishu = jishu,
                zhiye1 = zhiye1,
                zhiye2 = zhiye2,
                daxue = daxue,
                jingli = jingli,
                guanxi = guanxi,
                techang = techang,
                jiangfa = jiangfa,
                shenhe = shenhe,
                beizhu = beizhu
            )
            return render(req, 'zzb/mydata.html', {'userextend': userextend})
        else:
            if logourl:
                user.logo = logourl
                user.save()
            userextend = userextendlist.first()
            joinjob = zzJoinJob.objects.filter(user=userextend)
            if len(joinjob) == 0:
                pass
            else:
                joinjob.delete()

            userextend.name = name
            userextend.sex = sex
            userextend.minzu = minzu
            userextend.chusheng = chusheng
            userextend.jiguan = jiguan
            userextend.mianmao = mianmao
            userextend.huji = huji
            userextend.note1 = note1
            userextend.hunyin = hunyin
            userextend.idcard = idcard
            userextend.phone = dianhua
            userextend.tongxun = tongxun
            userextend.youbian = youbian
            userextend.xuexiao = xuexiao
            userextend.biye = biye
            userextend.zhuanye = zhuanye
            userextend.xueli = xueli
            userextend.waiyu = waiyu
            userextend.jisuanji = jisuanji
            userextend.danwei = danwei
            userextend.xingzhi = xingzhi
            userextend.luoshi = luoshi
            userextend.jiaozheng = jiaozheng
            userextend.shengao = shengao
            userextend.jishu = jishu
            userextend.zhiye1 = zhiye1
            userextend.zhiye2 = zhiye2
            userextend.daxue = daxue
            userextend.jingli = jingli
            userextend.guanxi = guanxi
            userextend.techang = techang
            userextend.jiangfa = jiangfa
            userextend.shenhe = shenhe
            userextend.beizhu = beizhu
            userextend.save()
            return render(req, 'zzb/mydata.html', {'userextend':userextend})



def time_set(req):
    try:
        timeList = zzTime.objects.get(id = 1)
    except:
        now = datetime.datetime.now()
        timeList = zzTime.objects.create(id = 1,startbm=now,
                                         endbm=now,startbs=now,
                                         endbs=now,startdy=now,
                                         enddy=now,startcj=now,
                                         endcj=now,
                                         )
    if req.method == 'GET':
        return render(req, 'zzb/time_set.html',
                      {'timeList':timeList})
    else:
        try:
            startbm = req.POST.get('met_startbm', None)
            endbm = req.POST.get('met_endbm', None)
            startdy = req.POST.get('met_startdy', None)
            enddy = req.POST.get('met_enddy', None)
            startbs = req.POST.get('met_startbs', None)
            endbs = req.POST.get('met_endbs', None)
            startcj = req.POST.get('met_startcj', None)
            endcj = req.POST.get('met_endcj', None)
        except:
            pass

        timeList.startbm = datetime.datetime.strptime(startbm, '%Y-%m-%d %H:%M:%S')
        timeList.endbm = datetime.datetime.strptime(endbm, '%Y-%m-%d %H:%M:%S')
        timeList.startdy = datetime.datetime.strptime(startdy, '%Y-%m-%d %H:%M:%S')
        timeList.enddy = datetime.datetime.strptime(enddy, '%Y-%m-%d %H:%M:%S')
        timeList.startbs = datetime.datetime.strptime(startbs, '%Y-%m-%d %H:%M:%S')
        timeList.endbs = datetime.datetime.strptime(endbs, '%Y-%m-%d %H:%M:%S')
        timeList.startcj = datetime.datetime.strptime(startcj, '%Y-%m-%d %H:%M:%S')
        timeList.endcj = datetime.datetime.strptime(endcj, '%Y-%m-%d %H:%M:%S')
        timeList.save()
        answer = '考试时间已更新'
        return render(req, 'zzb/time_set.html',
                      {'timeList':timeList,'answer':answer})


def database_set(req):
    zzUserCount = zzUser.objects.exclude(power=4).count()
    return render(req, 'zzb/database_set.html', {'zzUserCount':zzUserCount})

def cleanUser(req):
    zzUserList = zzUser.objects.exclude(power=4)
    for user in zzUserList:
        user.delete()
    return redirect('zzb:database_set')