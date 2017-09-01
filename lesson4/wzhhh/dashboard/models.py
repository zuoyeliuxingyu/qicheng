from django.db import models

# Create your models here.
'''
class Person(models.Model):
    #username  varchar(32) not null
    username = models.CharField(max_length=32, null=True) #模型字段
    first_name = models.CharField("person's first name", max_length=30, null=True)
    sec_name = models.CharField(max_length=30, null=True)

    class Meta:
        ordering = ["?ordering"]
        db_table = "person"
    #tablename = app_name + "_" + Person = dashboard_person
'''