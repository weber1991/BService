# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Screlation(models.Model):
    counterno = models.CharField(db_column='CounterNo', max_length=100, verbose_name='窗口编号')  # Field name made lowercase.
    serviceno = models.CharField(db_column='ServiceNo', max_length=100, verbose_name='业务编号')  # Field name made lowercase.
    servicename = models.CharField(db_column='ServiceName', max_length=500, blank=True, null=True, verbose_name='业务名称')  # Field name made lowercase.
    serviceid = models.IntegerField(db_column='ServiceId', primary_key=True, verbose_name='业务排序号')  # Field name made lowercase.

    class Meta:
        # verbose_name = u'业务与窗口对应关系 will be error ,it has the 's' in the end
        verbose_name_plural = '业务与窗口对应关系'
        managed = True
        db_table = 'screlation'
        unique_together = (('counterno', 'serviceno', 'serviceid'),)

    def __str__(self):
        return self.servicename


class Service(models.Model):
    serviceno = models.IntegerField(db_column='ServiceNo', primary_key=True)  # Field name made lowercase.
    servicetype = models.CharField(db_column='ServiceType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    digitlength = models.IntegerField(db_column='DigitLength', blank=True, null=True)  # Field name made lowercase.
    servicename = models.CharField(db_column='ServiceName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    workflowtext = models.CharField(db_column='WorkflowText', max_length=756, blank=True, null=True)  # Field name made lowercase.
    workflowcounter = models.CharField(db_column='WorkflowCounter', max_length=512, blank=True, null=True)  # Field name made lowercase.
    buttonleft = models.IntegerField(db_column='ButtonLeft', blank=True, null=True)  # Field name made lowercase.
    buttontop = models.IntegerField(db_column='ButtonTop', blank=True, null=True)  # Field name made lowercase.
    buttonwidth = models.IntegerField(db_column='ButtonWidth', blank=True, null=True)  # Field name made lowercase.
    buttonheight = models.IntegerField(db_column='ButtonHeight', blank=True, null=True)  # Field name made lowercase.
    locationtemplate = models.IntegerField(db_column='LocationTemplate', blank=True, null=True)  # Field name made lowercase.
    buttonbg = models.TextField(db_column='ButtonBG', blank=True, null=True)  # Field name made lowercase.
    buttonshowtext = models.IntegerField(db_column='ButtonShowText', blank=True, null=True)  # Field name made lowercase.
    tickettemplate = models.TextField(db_column='TicketTemplate', blank=True, null=True)  # Field name made lowercase.
    amlimit = models.IntegerField(db_column='AMLimit', blank=True, null=True)  # Field name made lowercase.
    amstarttime = models.DateTimeField(db_column='AMStartTime', blank=True, null=True)  # Field name made lowercase.
    amendtime = models.DateTimeField(db_column='AMEndTime', blank=True, null=True)  # Field name made lowercase.
    amtotal = models.IntegerField(db_column='AMTotal', blank=True, null=True)  # Field name made lowercase.
    pmlimit = models.IntegerField(db_column='PMLimit', blank=True, null=True)  # Field name made lowercase.
    pmstarttime = models.DateTimeField(db_column='PMStartTime', blank=True, null=True)  # Field name made lowercase.
    pmendtime = models.DateTimeField(db_column='PMEndTime', blank=True, null=True)  # Field name made lowercase.
    pmtotal = models.IntegerField(db_column='PMTotal', blank=True, null=True)  # Field name made lowercase.
    printpause = models.IntegerField(db_column='PrintPause', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=128, blank=True, null=True)  # Field name made lowercase.
    fontcolor = models.CharField(db_column='FontColor', max_length=32, blank=True, null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID', blank=True, null=True)  # Field name made lowercase.
    havechild = models.IntegerField(db_column='HaveChild', blank=True, null=True)  # Field name made lowercase.
    field_mask_to_v2 = models.DateTimeField(db_column='_MASK_TO_V2', blank=True, null=True)  # Field name made lowercase. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'service'

    def __str__(self):
        return self.serviceno


class Ticket(models.Model):
    ticketno = models.CharField(db_column='TicketNo', primary_key=True, max_length=32)  # Field name made lowercase.
    serviceno = models.IntegerField(db_column='ServiceNo', blank=True, null=True)  # Field name made lowercase.
    printtime = models.DateTimeField(db_column='PrintTime')  # Field name made lowercase.
    queuetime = models.DateTimeField(db_column='QueueTime', blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True)  # Field name made lowercase.
    finishedtime = models.DateTimeField(db_column='FinishedTime', blank=True, null=True)  # Field name made lowercase.
    cometime = models.CharField(db_column='ComeTime', max_length=512, blank=True, null=True)  # Field name made lowercase.
    processedtime = models.CharField(db_column='ProcessedTime', max_length=512, blank=True, null=True)  # Field name made lowercase.
    processedcounter = models.CharField(db_column='ProcessedCounter', max_length=256, blank=True, null=True)  # Field name made lowercase.
    processedstaffid = models.CharField(db_column='ProcessedStaffID', max_length=512, blank=True, null=True)  # Field name made lowercase.
    processingstatus = models.IntegerField(db_column='ProcessingStatus', blank=True, null=True)  # Field name made lowercase.
    lastcounter = models.IntegerField(db_column='LastCounter', blank=True, null=True)  # Field name made lowercase.
    processing = models.IntegerField(db_column='Processing', blank=True, null=True)  # Field name made lowercase.
    nextworkflow = models.CharField(db_column='NextWorkflow', max_length=512, blank=True, null=True)  # Field name made lowercase.
    nextcounter = models.CharField(db_column='NextCounter', max_length=256, blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    paused = models.IntegerField(db_column='Paused', blank=True, null=True)  # Field name made lowercase.
    customerrating = models.CharField(db_column='CustomerRating', max_length=256, blank=True, null=True)  # Field name made lowercase.
    delaybytime = models.IntegerField(db_column='DelayByTime', blank=True, null=True)  # Field name made lowercase.
    delaywayvalue = models.IntegerField(db_column='DelayWayValue', blank=True, null=True)  # Field name made lowercase.
    delaystarttime = models.DateTimeField(db_column='DelayStartTime', blank=True, null=True)  # Field name made lowercase.
    delayticketspassed = models.IntegerField(db_column='DelayTicketsPassed', blank=True, null=True)  # Field name made lowercase.
    parameters = models.CharField(db_column='Parameters', max_length=256, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=32, blank=True, null=True)  # Field name made lowercase.
    regtime = models.CharField(db_column='RegTime', max_length=16, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=32, blank=True, null=True)  # Field name made lowercase.
    reexam = models.IntegerField(db_column='Reexam', blank=True, null=True)  # Field name made lowercase.
    mobilephone = models.CharField(db_column='MobilePhone', max_length=16, blank=True, null=True)  # Field name made lowercase.
    smsresult = models.IntegerField(db_column='SmsResult', blank=True, null=True)  # Field name made lowercase.
    smstimes = models.IntegerField(db_column='SmsTimes', blank=True, null=True)  # Field name made lowercase.
    reservationstarttime = models.DateTimeField(db_column='ReservationStartTime', blank=True, null=True)  # Field name made lowercase.
    reservationendtime = models.DateTimeField(db_column='ReservationEndTime', blank=True, null=True)  # Field name made lowercase.
    reservationno = models.CharField(db_column='ReservationNo', max_length=32, blank=True, null=True)  # Field name made lowercase.
    field_mask_to_v2 = models.DateTimeField(db_column='_MASK_TO_V2', blank=True, null=True)  # Field name made lowercase. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'ticket'
        unique_together = (('ticketno', 'printtime'),)
        get_latest_by = 'printtime'