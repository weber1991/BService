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

    def __unicode__(self):
        return self.servicename
