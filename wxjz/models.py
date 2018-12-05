from django.db import models

# Create your models here.


class wxjz_type(models.Model):
    name = models.CharField(max_length=255, verbose_name='大类型')
    orderid = models.IntegerField(default=10, verbose_name='排序号')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '微信矩阵类型'
        verbose_name = '微信矩阵类型'
        ordering = ['orderid']


class wxjz(models.Model):
    type = models.ForeignKey(wxjz_type, verbose_name='类型')
    name = models.CharField(max_length=255, verbose_name='名称')
    url = models.CharField(max_length=512, verbose_name='链接')
    logo = models.ImageField(upload_to='wxjz', verbose_name='图标')
    orderid = models.IntegerField(verbose_name='排序号', default=10)
    note = models.TextField(verbose_name='备注', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '矩阵点名称'
        verbose_name_plural = '矩阵点名称'
        ordering = ['orderid']