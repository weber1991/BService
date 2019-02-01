# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-01-31 09:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='wxjz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('url', models.CharField(max_length=512, verbose_name='链接')),
                ('logo', models.ImageField(upload_to='wxjz', verbose_name='图标')),
                ('orderid', models.IntegerField(default=10, verbose_name='排序号')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '矩阵点名称',
                'verbose_name_plural': '矩阵点名称',
                'ordering': ['orderid'],
            },
        ),
        migrations.CreateModel(
            name='wxjz_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='大类型')),
                ('orderid', models.IntegerField(default=10, verbose_name='排序号')),
            ],
            options={
                'verbose_name': '微信矩阵类型',
                'verbose_name_plural': '微信矩阵类型',
                'ordering': ['orderid'],
            },
        ),
        migrations.AddField(
            model_name='wxjz',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wxjz.wxjz_type', verbose_name='类型'),
        ),
    ]