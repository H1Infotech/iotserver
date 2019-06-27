from django.urls import path,include
import backend.views.AccessManager as AccessManager
import backend.views.controller as controller
urlpatterns = [
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
]                           