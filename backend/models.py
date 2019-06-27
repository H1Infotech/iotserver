from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# 继承了内部用户管理类的拓展，添加新的自定义用户信息字段，减少多表关联的问题

class User(AbstractUser):
    phone = models.BigIntegerField('手机号', blank=False)
    
    class Meta:
        app_label = 'backend'


class Instrument(models.Model):
    userid = models.IntegerField(blank=False)        # 用户ID
    sensorid = models.CharField(blank=True,max_length=100)   # 设备编号
    mspoint = models.CharField(blank=True,max_length=600)    # 观测点
    work = models.IntegerField(blank=True)     # 工程ID
    project = models.IntegerField(blank=True) # 项目ID

    class Meta:
        app_label = 'backend'


class Project(models.Model):
            # 用户ID
    projectid = models.AutoField(primary_key=True) # 项目ID
    projectname = models.CharField(blank=False,max_length=50)
    userid = models.IntegerField(blank=False)
    create_time = models.DateField(blank=False)
    class Meta:
        app_label = 'backend'


class Work(models.Model):
    workid = models.AutoField(primary_key=True)
    userid = models.IntegerField(blank=False)        # 用户ID
    projectid = models.IntegerField(blank=False)  # 项目ID
    workname = models.CharField(blank=False,max_length=50)
    start_time = models.CharField(blank=False,max_length=100)
    end_time = models.CharField(blank=False,max_length=100)
    create_time = models.DateField(blank=False)
    class Meta:
        app_label = 'backend'

class Measurement(models.Model):
    mesureid = models.AutoField(primary_key=True) #测位点
    userid = models.IntegerField(blank=False)        # 用户ID
    projectid = models.IntegerField(blank=False) # 项目ID
    workid = models.IntegerField(blank=False) # 项目ID
    mesuredesc = models.CharField(blank=False,max_length=100)
    create_time = models.DateField(blank=False)
    class Meta:
        app_label = 'backend'

class DevRegister(models.Model):
    uuid = models.AutoField(primary_key=True)
    sensorid = models.CharField(blank=False,max_length=100)
    code = models.CharField(blank=False,max_length=100)
    regist_status = models.BooleanField(default=False)
    userid = models.IntegerField(blank=False) 
    class Meta:
        app_label = 'backend'


class DevTmpType(models.Model):
    uuid = models.AutoField(primary_key=True)
    sensorid = models.CharField(blank=False,max_length=100)
    tmp1 = models.IntegerField(blank=True)
    tmp2 = models.IntegerField(blank=True)
    tmp3 = models.IntegerField(blank=True)
    tmp4 = models.IntegerField(blank=True)
    tmp5 = models.IntegerField(blank=True)
    tmp6 = models.IntegerField(blank=True)
    tmp7 = models.IntegerField(blank=True)
    tmp8 = models.IntegerField(blank=True)
    class Meta:
        app_label = 'backend'