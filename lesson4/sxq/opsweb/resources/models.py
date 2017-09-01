# coding:utf8
from django.db import models

# Create your models here.

class Idc(models.Model):
    id
    name = models.CharField("idc 简称", max_length=10, default="", db_index=True, unique=True)
    idc_name = models.CharField("idc 名字", max_length=50, default="")
    address = models.CharField("address", max_length=255, null=True)
    phone = models.CharField("idc phone", max_length=20, null=True)
    email = models.EmailField("idc email", null=True)
    username = models.CharField("idc 联系人",max_length=32, null=True)
    remark = models.CharField("remark", max_length=100, default="")

    class Meta:
        db_table = "resources_idc"
