from django.db import models

# Create your models here.
class Idc(models.Model):
    """ IDC 表结构 model"""
    name = models.CharField("idc 字母简称", max_length=10, default="", db_index=True)   # 唯一索引
    idc_name = models.CharField("idc 中文", max_length=32, default="")
    address = models.CharField("具体的地址", max_length=255, default="")
    phone = models.CharField("机房的联系电话", max_length=20, default="")
    email = models.EmailField("机房联系人邮件", max_length=50, default="", null=True)
    username = models.CharField("机房联系人", max_length=32, null=True)

    class Meta:
        db_table = "resources_idc"      # 数据库表名
