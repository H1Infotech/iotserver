from django.shortcuts import render
from backend.toolkits.AjaxResponse import AjaxResponse
from backend.models import Instrument,Project,Work,Measurement,DevRegister,DevTmpType
import datetime
import json
from django.forms.models import model_to_dict 
from django.core import serializers 
import redis
from postgres import Postgres
import copy

# 获取IOT设备监听数据方法接入口
cur = Postgres("postgres://{}:{}@{}:{}/{}".format('postgres','postgres','47.100.247.139','8660','platform'))
pool = redis.ConnectionPool(host='47.100.247.139',port=5432, db=0,password='123qweasdzxc')
r = redis.Redis(connection_pool=pool)


# 注册项目
def project_register(request) -> None:
    
    # 判断请求方法为POST方法
    datetimes = datetime.datetime.now().date()
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.session['userid']
            try:
                projectname = request.POST['projectName']
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
                Project.objects.get_or_create(userid=userid,projectname=projectname,create_time=datetimes)
                data = {'userid':userid,'projectname':projectname}
                return AjaxResponse().successMessage(data=data)
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 查找项目
def project_get(request) -> None:
    # 判断请求方法为POST方法
    datetimes = datetime.datetime.now().date()
    if request.method == 'GET':
        if request.user.is_authenticated:
            userid = request.session['userid']       
            try:
                result = Project.objects.filter(userid=userid)
                data = serializers.serialize("json",result)
                return AjaxResponse().successMessage(data=data)
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 删除项目
def project_del(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.session['userid']   
            try:
                projectid = request.POST['projectId']    
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
               Project.objects.filter(userid=userid,projectid=projectid).delete()
               Work.objects.filter(userid=userid,projectid=projectid).delete()
               Measurement.objects.filter(userid=userid,projectid=projectid).delete()
               Instrument.objects.filter(userid=userid,projectid=projectid).delete()
               return AjaxResponse().successMessage()
            except Exception as identifier:
                return AjaxResponse().successMessage()
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 注册工程
def work_register(request) -> None:
    # 判断请求方法为POST方法
    datetimes = datetime.datetime.now().date()
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.session['userid']
            try:
                projectid = request.POST['projectId']
                workname = request.POST['workName']
                start_time = request.POST['start_time']
                end_time = request.POST['end_time']
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
                Work.objects.get_or_create(userid=userid,projectid=projectid,workname=workname,create_time=datetimes,start_time=start_time,end_time=end_time)
                data = {'userid':userid,'projectID':projectid,'workname':workname}
                return AjaxResponse().successMessage(data=data)
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 查找工程
def work_get(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'GET':
        if request.user.is_authenticated:
            userid = request.session['userid']
            try:
                projectid = request.GET.get('projectId')       
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
                result = Work.objects.filter(userid=userid,projectid=projectid)
                data = serializers.serialize("json",result)
                return AjaxResponse().successMessage(data=data)
           
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 删除工程
def work_del(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'POST':
        if request.user.is_authenticated:
           userid = request.session['userid']   
           try:
                projectid = request.POST['projectId']
                workid = request.POST['workId']   
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)     
           try:
               Work.objects.filter(userid=userid,projectid=projectid,workid=workid).delete()
               Measurement.objects.filter(userid=userid,projectid=projectid,workid=workid).delete()
               Instrument.objects.filter(userid=userid,projectid=projectid,workid=workid).delete()
               return AjaxResponse().successMessage()
           except Exception as identifier:
               return AjaxResponse().successMessage()
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 注册测位点
def measure_register(request) -> None:
    # 判断请求方法为POST方法
    datetimes = datetime.datetime.now().date()
    if request.method == 'POST':
        if request.user.is_authenticated:
           userid = request.session['userid']
           try:
                projectid = request.POST['projectId']
                workid = request.POST['workId']
                mesuredesc = request.POST['mesureDesc']
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
           try:
               Measurement.objects.get_or_create(userid=userid,projectid=projectid,workid=workid,mesuredesc=mesuredesc,create_time=datetimes)
               data = {'userid':userid,'projectID':projectid,'workid':workid,'mesuredesc':mesuredesc}
               return AjaxResponse().successMessage(data=data)
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 查找测位点
def measure_get(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'GET':
        if request.user.is_authenticated:
            userid = request.session['userid']
            try:
                projectid = request.GET.get('projectId')
                workid =   request.GET.get('workId')      
            except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)     
            try:
               result = Measurement.objects.filter(userid=userid,projectid=projectid,workid=workid)
               data = serializers.serialize("json",result)
               return AjaxResponse().successMessage(data=data)
            except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 删除测位点
def measure_del(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'POST':
        if request.user.is_authenticated:
           userid = request.session['userid']   
           try:
                projectid = request.POST['projectId']
                workid = request.POST['workId']
                mesureid =  request.POST['mesureId']
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
           try:
               Measurement.objects.filter(userid=userid,projectid=projectid,workid=workid,mesureid=mesureid).delete()
               Instrument.objects.filter(userid=userid,projectid=projectid,workid=workid,mesureid=mesureid).delete()
               return AjaxResponse().successMessage()
           except Exception as identifier:
               return AjaxResponse().successMessage()
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 注册仪器
def instrument_register(request) -> None:
    # 判断请求方法为POST方法
    datetimes = datetime.datetime.now().date()
    if request.method == 'POST':
        if request.user.is_authenticated:
           userid = request.session['userid']
           try:
                projectid = request.POST['projectId']
                workid = request.POST['workId']
                mesureid = request.POST['mesureId']
                sensorid = request.POST['sensorId']
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
           try:
               Instrument.objects.get_or_create(userid=userid,project=projectid,work=workid,mspoint=mesureid,sensorid=sensorid)
               data = {'userid':userid,'projectID':projectid,'workid':workid,'mesureid':mesureid,'sensorid':sensorid}
               return AjaxResponse().successMessage(data=data)
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 查找仪器
def instrument_get(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'GET':
        if request.user.is_authenticated:
           userid = request.session['userid']
           try:
                projectid = request.GET.get('projectId')
                mesureid = request.GET.get('mesureId') 
                workid = request.GET.get('workId')       
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
           try:
               result = Instrument.objects.filter(userid=userid,project=projectid,mspoint=mesureid,work=workid)
               data = serializers.serialize("json",result)
               return AjaxResponse().successMessage(data=data)
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 删除仪器
def instrument_del(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.session['userid']   
            try:
                projectid = request.POST['projectId']
                workid = request.POST['workId']
                mesureid =  request.POST['mesureId']
                sensorid = request.POST['sensorId']
            except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
            try:
               Instrument.objects.filter(userid=userid,project=projectid,work=workid,mspoint=mesureid,sensorid=sensorid).delete()
               return AjaxResponse().successMessage()
            except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 同步数据
def device_info(request) -> None:
    # 判断请求方法为POST方法
    if request.method == 'GET':
        if request.user.is_authenticated:
            userid = request.session['userid']   
            try:
                deviceid = request.GET.get('deviceID')
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
                result = r.get(deviceid)
                return AjaxResponse().successMessage(data=json.loads(result))
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 注册方法，用户注册码注册仪器，记录注册状态
def device_register(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.session['userid']   
            # 验证输入参数 是否正确
            try:
                sensorid = request.POST['sensorId']
                code = request.POST['code']
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
           
           # view 层操作数据去注册表      
            try:   
                result = DevRegister.objects.filter(sensorid=sensorid,code=code)
                if result.regist_status == False:
                    DevRegister.objects.filter(sensorid=sensorid).update(regist_status=True,userid=userid)
                    return AjaxResponse().successMessage(message="注册成功")
                
                elif result.regist_status == True:
                    return AjaxResponse().successMessage(message="设备已经被注册")
                else:
                    return AjaxResponse().successMessage(message="设备ID输入错误")
            except Exception as identifier:
                return AjaxResponse().errorMessage(error="注册无效")    
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 查找返回用户尚未注册的设备
def device_register_check(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            userid = request.session['userid']   
             # 直接获取用户id
             # view 层操作数据去注册表
            user_device_registed_list = list()
            user_owned_list = list()       
            try:
                user_device_owned = Instrument.objects.filter(userid=userid).exclude(sensorid="")
                user_device_table_registed = DevRegister.objects.filter(userid=userid,)
                user_owned_list = [i.sensorid for i in user_device_owned]
                user_device_registed_list = [i.sensorid for i in user_device_table_registed]
                result = list(set(user_owned_list).difference(set(user_device_registed_list)))
                return AjaxResponse().successMessage(data=result)
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)    
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 用户离线同步
def pull_data(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.session['userid']
            try:
                time_start = request.POST['time_start'] # 年月日
                time_end = request.POST['time_end'] #年月日
                deviceid = request.POST['deviceid']
                time_start_list = time_start.split('-')
                start_year = time_start_list[0] # 年 
                start_month = time_start_list[1] # 月
                start_day = time_start_list[2] # 日
                time_end_list = time_end.split('-')
                end_year = time_end_list[0] # 年
                end_month = time_end_list[1] # 月
                end_day = time_end_list[2] # 日
                
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
                sql = "select * from device_info_test where (deviceid=\'{}\') and (year between \'{}\' and \'{}\') and (month between \'{}\' and \'{}\') and (day between \'{}\' and \'{}\')".format(deviceid,start_year,end_year,start_month,end_month,start_day,end_day)
                result = cur.all(sql)
                res_dict = {}
                tmp_dict = {}
                for i in result:
                    tmp_dict["hour"] = i.hour
                    tmp_dict["minute"] = i.minute
                    tmp_dict["secound"] = i.secound
                    tmp_dict["temp1"] = i.temp1
                    tmp_dict["temp2"] = i.temp2
                    tmp_dict["temp3"] = i.temp3
                    tmp_dict["temp4"] = i.temp4
                    tmp_dict["temp5"] = i.temp5
                    tmp_dict["temp6"] = i.temp6
                    tmp_dict["temp7"] = i.temp7
                    tmp_dict["temp8"] = i.temp8
                    tmp_dict["battery"] = i.battery
                    res_dict[i.id] = copy.deepcopy(tmp_dict)
                    tmp_dict.clear()
                return AjaxResponse().successMessage(json.dumps(res_dict))
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 用户设备通道信息标签设置
def device_tmp_put(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.session['userid']
            try:
                sensorid = request.POST['sensorid']
                tmp1 = request.POST['tmp1']
                tmp2 = request.POST['tmp2']
                tmp3 = request.POST['tmp3']
                tmp4 = request.POST['tmp4']
                tmp5 = request.POST['tmp5']
                tmp6 = request.POST['tmp6']
                tmp7 = request.POST['tmp7']
                tmp8 = request.POST['tmp8']
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
                DevTmpType.objects.get_or_create(uuid=userid,sensorid=sensorid,tmp1=tmp1,tmp2=tmp2,tmp3=tmp3,tmp4=tmp4,tmp5=tmp5,tmp6=tmp6,tmp7=tmp7,tmp8=tmp8)
                return AjaxResponse().successMessage("设置成功")
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")

# 用户设备通道信息标签设置
def device_tmp_get(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            userid = request.session['userid']
            try:
                sensorid = request.POST['sensorid']

            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
            try:
                result = DevTmpType.objects.filter(uuid=userid,sensorid=sensorid)
                data = serializers.serialize("json",result)
                return AjaxResponse().successMessage(data=data)
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)
        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")