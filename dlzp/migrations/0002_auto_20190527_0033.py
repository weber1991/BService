# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-27 00:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlzp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zztime',
            name='endbm',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496222), verbose_name='结束报名时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='endbs',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496357), null=True, verbose_name='结束笔试时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='endcj',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496424), verbose_name='结束查询时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='enddy',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496290), verbose_name='结束打印时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startbm',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496177), verbose_name='开始报名时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startbs',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496323), null=True, verbose_name='开始笔试时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startcj',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496391), verbose_name='开始查询时间'),
        ),
        migrations.AlterField(
            model_name='zztime',
            name='startdy',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 27, 0, 33, 8, 496256), verbose_name='开始打印时间'),
        ),
    ]