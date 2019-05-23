from django.db import models
import datetime
# Create your models here.

class zzTime(models.Model):
    name = models.CharField(max_length=255, verbose_name='招聘项目名称')
    startbm = models.DateTimeField(verbose_name='开始报名时间', default=datetime.datetime.now())
    endbm = models.DateTimeField(verbose_name='结束报名时间', default=datetime.datetime.now())
    startdy = models.DateTimeField(verbose_name='开始打印时间', default=datetime.datetime.now())
    enddy = models.DateTimeField(verbose_name='结束打印时间', default=datetime.datetime.now())
    startbs = models.DateTimeField(verbose_name='开始笔试时间', null=True, blank=True, default=datetime.datetime.now())
    endbs = models.DateTimeField(verbose_name='结束笔试时间', null=True, blank=True, default=datetime.datetime.now())
    startcj = models.DateTimeField(verbose_name='开始查询时间', default=datetime.datetime.now())
    endcj = models.DateTimeField(verbose_name='结束查询时间', default=datetime.datetime.now())
    state = models.BooleanField(verbose_name='项目状态', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '招聘项目时间流程'
        verbose_name_plural = '招聘项目时间流程'



class zzUser(models.Model):
    name = models.CharField(max_length=255, verbose_name='用户名',null=True,blank=True,default='')
    idcard = models.CharField(max_length=20,verbose_name='身份证', null=True,blank=True,default='')
    phone = models.CharField(max_length=11, verbose_name='手机号码',null=True,blank=True, default='')
    email = models.EmailField(verbose_name='电子邮箱', null=True,blank=True, default='')
    username = models.CharField(max_length=255, verbose_name='用户账号',null=True,blank=True, default='')
    password = models.CharField(max_length=255, verbose_name='用户密码',null=True,blank=True, default='')
    logo = models.ImageField(upload_to='BUser/logo', verbose_name='用户头像', default='BUser/logo/人.png')
    power = models.IntegerField(verbose_name='权限系数', default=0)
    hold0 = models.CharField(max_length=255, verbose_name='预留字段0',null=True,blank=True,default='')
    hold1 = models.CharField(max_length=255, verbose_name='预留字段1', null=True,blank=True, default='')
    hold2 = models.CharField(max_length=255, verbose_name='预留字段2', null=True,blank=True, default='')
    hold3 = models.CharField(max_length=255, verbose_name='预留字段3', null=True,blank=True, default='')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户记录'
        verbose_name_plural = '用户记录'

class zzWechatUser(models.Model):
    openid = models.CharField(max_length=255, verbose_name='用户识别号')
    name = models.CharField(max_length=255, verbose_name='用户名', null=True, blank=True, default='')
    idcard = models.CharField(max_length=20, verbose_name='身份证', null=True, blank=True, default='')
    phone = models.CharField(max_length=11, verbose_name='手机号码', null=True, blank=True, default='')
    email = models.EmailField(verbose_name='电子邮箱', null=True, blank=True, default='')
    power = models.IntegerField(verbose_name='权限系数', default=0)
    logo = models.ImageField(upload_to='BUser/logo', verbose_name='用户头像', default='BUser/logo/人.png')
    hold0 = models.CharField(max_length=255, verbose_name='预留字段0', null=True, blank=True, default='')
    hold1 = models.CharField(max_length=255, verbose_name='预留字段1', null=True, blank=True, default='')
    hold2 = models.CharField(max_length=255, verbose_name='预留字段2', null=True, blank=True, default='')
    hold3 = models.CharField(max_length=255, verbose_name='预留字段3', null=True, blank=True, default='')

    def __str__(self):
        if self.name is None:
            return self.openid
        else:
            return self.name

    class Meta:
        verbose_name = '微信用户'
        verbose_name_plural = '微信用户'


'''
2018年招编外工作人员报名表-个人资料表
与人员关系为一对一
1、编辑个人信息
2、判断是否已经报名的情况：
    a、以身份证号码为唯一标准；（身份证自动带入，但可以修改。）
    b、每个账号只能报名一次；
3、表单的验证：
    a、身份证的校验；
    b、表单是否为空校验；

'''
class zzUserExtend(models.Model):
    user = models.OneToOneField(zzUser, verbose_name='用户')
    name = models.CharField(max_length=255, verbose_name='姓名', default='')
    sex = models.CharField(max_length=10, verbose_name='性别', default='')
    minzu = models.CharField(max_length=10, verbose_name='民族', default='')
    chusheng = models.CharField(max_length=255,verbose_name='出生年月', default='')
    jiguan = models.CharField(max_length=255, verbose_name='籍贯', default='')
    mianmao = models.CharField(max_length=255, verbose_name='政治面貌', default='')
    huji = models.CharField(max_length=255, verbose_name='现户籍地', default='')
    hunyin = models.CharField(max_length=255, verbose_name='婚姻状况', default='')
    logo = models.ImageField(max_length=255, verbose_name='彩照', default='')
    idcard = models.CharField(max_length=255, verbose_name='身份证', default='')
    phone = models.CharField(max_length=255, verbose_name='联系电话', default='')
    tongxun = models.CharField(max_length=255, verbose_name='通讯地址', default='')
    youbian = models.CharField(max_length=255, verbose_name='邮编', default='')
    xuexiao = models.CharField(max_length=255, verbose_name='毕业院校', default='')
    biye = models.CharField(max_length=255, verbose_name='毕业时间', default='')
    zhuanye = models.CharField(max_length=255, verbose_name='所学专业', default='')
    xueli = models.CharField(max_length=255, verbose_name='学历及学位', default='')
    waiyu = models.CharField(max_length=255, verbose_name='外语水平', default='')
    jisuanji = models.CharField(max_length=255, verbose_name='计算机水平', default='')
    danwei = models.CharField(max_length=255, verbose_name='工作单位', default='')
    xingzhi = models.CharField(max_length=255, verbose_name='单位性质', default='')
    luoshi = models.CharField(max_length=255, verbose_name='裸视视力', default='')
    jiaozheng = models.CharField(max_length=255, verbose_name='矫正视力', default='')
    shengao = models.CharField(max_length=255, verbose_name='身高', default='')
    jishu = models.CharField(max_length=255, verbose_name='专业技术资格', default='')
    zhiye1 = models.CharField(max_length=255, verbose_name='职业资格', default='')
    zhiye2 = models.CharField(max_length=255, verbose_name='执业资格', default='')
    daxue = models.TextField(verbose_name='大学担任职务', default='')
    jingli = models.TextField(verbose_name='学习、工作经历', default='')
    guanxi = models.TextField(verbose_name='成员关系', default='')
    techang = models.TextField(verbose_name='特长及突出业绩', default='')
    jiangfa = models.TextField(verbose_name='奖罚情况', default='')
    shenhe = models.TextField(verbose_name='审核意见', default='')
    beizhu = models.TextField(verbose_name='备注', default='')
    note1 = models.CharField(max_length=255, verbose_name='保留字段1', default='')
    note2 = models.CharField(max_length=255, verbose_name='保留字段2', default='')
    note3 = models.TextField(verbose_name='保留字段3', default='')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name= '个人信息表'
        verbose_name_plural = verbose_name


class zzNotice(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.CharField(max_length=255, verbose_name='发布人')
    state = models.CharField(max_length=25, verbose_name='文章状态')

    objects = models.Manager()

    class Meta:
        verbose_name = '通知公告'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title

'''
1、到期时间暂代
2、状态：草稿-发布
'''
class zzJob(models.Model):
    daihao = models.CharField(max_length=255, verbose_name='岗位代号')
    name = models.CharField(max_length=255, verbose_name='招考岗位')
    count = models.CharField(max_length=5, verbose_name='招聘人数')
    education = models.CharField(max_length=255, verbose_name='学历要求')
    major = models.CharField(max_length=512, verbose_name='专业要求')
    other = models.TextField(verbose_name='其他要求')
    note = models.TextField(verbose_name='备注')
    state = models.CharField(max_length=63, verbose_name='状态')
    outtime = models.DateTimeField(verbose_name='到期时间', null=True, blank=True)
    hold0 = models.CharField(max_length=255, null=True, blank=True, verbose_name='最低年龄限制条件', default='保留')
    hold1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='保留字段', default='保留')
    hold2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='保留字段', default='保留')
    hold3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='保留字段', default='保留')


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '招聘岗位'
        verbose_name_plural = verbose_name



'''
报名的序列：
1、与岗位是一对多关系
2、与人员是一对一关系
3、状态：提交报名-打印准考证
    a、待审核的时候，可以修改，一旦审核通过，无法修改。
    b、时间超过则无法修改。（自动化的操作和手动操作）
4、考试状态：笔试-面试-体检-政审-入职
5、
'''
class zzJoinJob(models.Model):
    job = models.ForeignKey(zzJob, verbose_name='招聘岗位')
    user = models.OneToOneField(zzUserExtend, verbose_name='报考人员')
    # 待审核-通过-等待打印准考证-打印准考证
    state = models.CharField(max_length=63, verbose_name='状态', default='待审核')
    sweat = models.CharField(max_length=255, verbose_name='考试座位', default='待定')
    score = models.CharField(max_length=10, verbose_name='考试分数', default='待定')
    process = models.CharField(max_length=52, verbose_name='招聘进度', default='笔试')
    note = models.CharField(max_length=255, verbose_name='备注', default='无')
    zkzh = models.CharField(max_length=255, verbose_name='准考证号', default='XXXX******####')


    def __str__(self):
        return '%s报考%s岗位，分数为%s。'%(self.user.name,self.job,self.score)

    class Meta:
        verbose_name = '报名单'
        verbose_name_plural = verbose_name


class zzSysBase(models.Model):
    '''
    ·系统基本配置类，记录系统基本信息。
    ·如：报名表标题，警示语，考试时间，地点等。
    '''
    name = models.CharField(max_length=128, verbose_name='配置选项', default='待定')
    content = models.TextField(verbose_name='配置内容')
    note = models.TextField(verbose_name='备注', default = '',null = True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '系统基本配置'
        verbose_name_plural = verbose_name