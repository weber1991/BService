# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-18 14:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zzb', '0002_auto_20190131_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zztime',
            name='endbm',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 18, 14, 40, 3, 460460), verbose_name='结束报名时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='endbs',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 18, 14, 40, 3, 461459), null=True, verbose_name='结束笔试时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='endcj',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 18, 14, 40, 3, 461459), verbose_name='结束查询时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='enddy',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 18, 14, 40, 3, 461459), verbose_name='结束打印时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startbm',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 18, 14, 40, 3, 460460), verbose_name='开始报名时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startbs',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 18, 14, 40, 3, 461459), null=True, verbose_name='开始笔试时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startcj',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 18, 14, 40, 3, 461459), verbose_name='开始查询时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startdy',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 18, 14, 40, 3, 460460), verbose_name='开始打印时间'),
        ),
    ]