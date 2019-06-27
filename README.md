# iotserver
基于Django框架开发的IOT 传感器项目



##### 项目依赖以及运行环境

1. nginx Stable version 1.16.0 + uswgi

2. PostgreSQL-10 数据库

3. redis 缓存服务器

4. celery 服务



##### 模块功能- 监听器

独立的监听器用作接受请求，在 iotserver/listener，支持异步解析并且直接将解析后的数据存放入数据库中

> DataParser.py 解析数据

> insert.py 用作自动创建表以及插入数据功能

> tasks.py 用作异步任务运行

> UDPListener.py 用作socket服务，并且把数据抛给celery 队列作为处理

⚠️ 在UDPListener.py 中 服务器作为上位机并未能返回数据给客户端，需要按照规定返回 数据条数，以及时间



##### 模块功能-AP接口



toolkits / AjaxResponse 为封装的Response 方法

Django 框架下的基本API接口模块

```python
path('user/register',AccessManager.register),
path('user/login',AccessManager.user_login),
path('user/logout',AccessManager.user_logout),
path('user/update',AccessManager.user_update),
path('user/info',AccessManager.user_info),
path('project/register',controller.project_register),
path('project/get',controller.project_get),
path('project/del',controller.project_del),
path('work/register',controller.work_register),
path('work/get',controller.work_get),
path('work/del',controller.work_del),
path('measure/register',controller.measure_register),
path('measure/get',controller.measure_get),
path('measure/del',controller.measure_del),
path('instrument/register',controller.instrument_register),
path('instrument/get',controller.instrument_get),
path('instrument/del',controller.instrument_del),
path('device_info/get',controller.device_info),
path('device_info/pull',controller.pull_data),
path('device/register',controller.device_register),
path('device/check_unregi',controller.device_register_check),
path('device/setting_update',controller.device_tmp_put),
path('device/setting_get',controller.device_tmp_get),
```



接口主要分为基础用户管理，项目管理，工程管理，测位点管理，设备管理，  设备注册接受请求 为device 相关

⚠️ 换里表设置 (环1 里2 表3) 已经写好， 缺少 峰值信息 需要再出一个 models，用来存储用户定位的峰值 查找对应表的位置即可

以下是接口测试相关参数信息 有待补充

```javascript
curl --location --request POST "47.100.247.139:8088/api/user/register" \
  --form "username=test" \
  --form "password=123" \
  --form "email=a@gmail.com" \
  --form "last_name=asd" \
  --form "first_name=qq" \
  --form "phone=18910067189"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/user/login" \
  --form "username=test5" \
  --form "password=1234"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/user/update" \
  --form "username=test5" \
  --form "password=1234" \
  --form "email=b@gmail.com" \
  --form "last_name=qq" \
  --form "first_name=asda" \
  --form "phone=18910981821"
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/user/info"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/project/register" \
  --form "projectName=测试项目123"
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/user/logout"
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/project/get"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/project/del" \
  --form "projectId=21"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/work/register" \
  --form "projectId=11" \
  --form "workName=asd" \
  --form "start_time=1998-03-11" \
  --form "end_time=1999-03-11"
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/work/get?projectId=11"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/work/del" \
  --form "projectId=11" \
  --form "workId=11"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/measure/register" \
  --form "projectId=11" \
  --form "workId=12" \
  --form "mesureDesc=侧位点上"
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/measure/get?projectId=11&workId=12"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/measure/del" \
  --form "projectId=" \
  --form "workId=" \
  --form "mesureId="
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/instrument/register" \
  --form "projectId=" \
  --form "workId=" \
  --form "mesureId=" \
  --form "sensorId="
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/instrument/get?projectId&mesureId&workId"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/instrument/del" \
  --form "projectId=" \
  --form "workId=" \
  --form "mesureId=" \
  --form "sensorId="
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/device_info/get?deviceID"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/device_info/pull" \
  --form "time_start=" \
  --form "time_end=" \
  --form "deviceid="
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/device/register" \
  --form "sensorId=" \
  --form "code="
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/device/check_unregi"
```

```javascript
curl --location --request POST "47.100.247.139:8088/api/device/setting_update" \
  --form "sensorid=" \
  --form "tmp1=" \
  --form "tmp2=" \
  --form "tmp3=" \
  --form "tmp4=" \
  --form "tmp5=" \
  --form "tmp6=" \
  --form "tmp7=" \
  --form "tmp8="
```

```javascript
curl --location --request GET "47.100.247.139:8088/api/device/setting_get?sensorid"
```