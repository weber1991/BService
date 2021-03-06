from django.conf.urls import url
from zzb.views import *


app_name = 'zzb'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^superme/$', superme, name='superme'),
    url(r'^login_weber/$', login, name='login'),
    url(r'^reset_password/$', reset_password, name='reset_password'),
    url(r'^set_password/$', set_password, name='set_password'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^zzb_temp/$', zzb_temp, name='zzb_temp'),
    url(r'^register/$', register, name='register'),
    url(r'^notice_list/',notice_list, name='notice_list'),
    url(r'^notice_list_all/', notice_list_all, name='notice_list_all'),
    url(r'^notice_look/(?P<id>[0-9]+)/$', notice_look, name='notice_look'),
    url(r'^notice_add/$', notice_add, name='notice_add'),
    url(r'^notice_editor/(?P<id>[0-9]+)/$', notice_editor, name='notice_editor'),
    url(r'^notice_change/(?P<id>[0-9]+)/$', notice_change, name='notice_change'),
    url(r'^notice_delete/(?P<id>[0-9]+)/$', notice_delete, name='notice_delete'),
    #url(r'^shixiang_change/(?P<bh>[0-9]+)/$',shixiang_change , name='shixiang_change'),
    #url(r'^loginmessage/$', loginMessage, name='loginmessage'),

    url(r'^job_list/$', job_list, name='job_list'),
    url(r'^job_list_all/$', job_list_all, name='job_list_all'),
    url(r'^job_add/$', job_add, name='job_add'),
    url(r'^job_change/(?P<id>[0-9]+)/$', job_change, name='job_change'),
    url(r'^job_editor/(?P<id>[0-9]+)/$', job_editor, name='job_editor'),
    url(r'^job_data/(?P<id>[0-9]+)/$', job_data, name='job_data'),
    url(r'^job_delete/(?P<id>[0-9]+)/$', job_delete, name='job_delete'),

    url(r'^join_job/', join_job, name='join_job'),
    url(r'^join_list/', join_list, name='join_list'),# 展示个人的报考情况
    url(r'^join_list_all/', join_list_all, name='join_list_all'), # 展示所有人的个人报考情况
    url(r'^join_success/(?P<id>[0-9]+)/$', join_success, name='join_success'),  # 审核通过
    url(r'^join_faile/(?P<id>[0-9]+)/$', join_faile, name='join_faile'), # 审核不通过
    url(r'^join_show/(?P<id>[0-9]+)/$', join_show, name='join_show'),  # 展示个人信息
    url(r'^join_count/$', join_count, name='join_count'), # 统计数据
    url(r'^join_job_count/(?P<id>[0-9]+)/$', join_job_count, name='join_job_count'), # 展示每个业务分别的报考人数
    url(r'^join_job_faile_list/$', join_faile_list, name = 'join_faile_list'), # 审核不通过名单
    url(r'^join_job_faile/$', joinjob_faile, name = 'join_faile'), # 添加审核不通过人员
    url(r'^join_reset/(?P<id>[0-9]+)/$', join_reset, name='join_reset'),  # 展示个人信息

    url(r'^seat_crate/$', seat_create, name='seat_crate'), # 生成座位
    url(r'^seat_list/$', seat_list, name='seat_list'), # 显示座位列表


    url(r'^paper_list/$', paper_list, name='paper_list'),
    url(r'^paper_list_all', paper_list_all, name='paper_list_all'),
    url(r'^paper_data/(?P<id>[0-9]+)/$', paper_data, name='paper_data'),


    url(r'^zzb_bmb/(?P<id>[0-9]+)/$', print_joinjob, name='print_joinjob'), # 打印报名表
    url(r'^zzb_zkz/(?P<id>[0-9]+)/$', print_zkz, name='print_zkz'),
    url(r'^zkz_set/$', zkz_set, name='zkz_set'), # 准考证配置

    url(r'^joinjob_excel/$', joinjob_excel, name='joinjob_excel'), # 导出数据
    url(r'^seat_excel/$', seat_excel, name='seat_excel'),  # 座位数据
    url(r'^seat_data_excel/$', seat_data_excel, name='seat_data_excel'),  # 座位数据

    url(r'^chengji_list/$', chengji_list, name='chengji_list'),  # 成绩导入
    url(r'chengji_data/$', chengji_data, name='chengji_data'),  # 成绩查询
    url(r'chengji_look/(?P<id>[0-9]+)/$', chengji_look, name='chengji_look'),  # 成绩查询,管理员用

    url(r'^mydata/$', mydata, name='mydata'),

    url(r'^time_set/$', time_set, name='time_set'),

    url(r'^database_set/$', database_set, name='database_set'),

    url(r'^cleanuser/$', cleanUser, name='cleanuser'),
]
