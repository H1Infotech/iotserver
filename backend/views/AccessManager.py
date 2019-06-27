from django.shortcuts import render
from backend.toolkits.AjaxResponse import AjaxResponse
from backend.models import User
from django.contrib.auth import authenticate, login, logout
import re
from django.core import serializers
import json
# Create your views here.

# 用户注册接口
# Headers Content-Tpye
# Body form-data
# @param username
# @param password
# @param email

def register(request) -> None:
    # 判断请求方法为POST方法
    """ 用户注册接口 """
    if request.method == 'POST':
        try:
            username = request.POST['username']  # 用户名
            password = request.POST['password']  # 密码
            email = request.POST['email']    # 邮箱
            last_name = request.POST['last_name']  # 姓
            first_name = request.POST['first_name']  # 名
            phone = request.POST['phone'] # 手机
            verify_email = re.match(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$',email,flags=0)
            verify_phone = re.match(r"^1[35678]\d{9}$", phone)
            if verify_email == None:
                return AjaxResponse().errorMessage(error="Wrong email address")
            if verify_phone == None:
                return AjaxResponse().errorMessage(error="Wrong Phone number")

        except Exception as identifier:
            return AjaxResponse().errorMessage(error=identifier)

        try:
            # 规定新建用户必要字段
            User.objects.create_user(username=username, password=password,
                                     email=email, last_name=last_name, first_name=first_name,phone=phone)
            data = {"username": username}
            return AjaxResponse().successMessage(data=data)

        except Exception as identifier:
            return AjaxResponse().errorMessage(error=identifier)
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")


def user_login(request) -> None:
    """ 用户登录接口 """
    if request.method == 'POST':
        username = request.POST['username']  # 用户名
        password = request.POST['password']  # 密码

        # 使用Django自带的 验证方法
        user = authenticate(request, username=username, password=password)
        # 判断用户是否注册过
        if user is not None:

            login(request, user)
            user = User.objects.get(username=username)
            request.session['userid'] = user.id
            data = {"username": username}
            return AjaxResponse().successMessage(data=data)

        else:
            data = {"username": username}
            return AjaxResponse().errorMessage(error="error", message="false", data=data)
    else:

        return AjaxResponse().errorMessage(error="Method Allow POST")

def user_update(request) -> None:
    """ 用户信息修改 """
    if request.method == 'POST':
        if request.user.is_authenticated:
           userid = request.session['userid']
           # 验证输入参数 是否正确
           try:
                username = request.POST['username']  # 用户名
                password = request.POST['password']  # 密码
                email = request.POST['email']    # 邮箱
                last_name = request.POST['last_name']  # 姓
                first_name = request.POST['first_name']  # 名
                phone = request.POST['phone'] # 手机
                verify_email = re.match(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$',email,flags=0)
                verify_phone = re.match(r"^1[35678]\d{9}$", phone)
                if verify_email == None:
                    return AjaxResponse().errorMessage(error="Wrong email address")
                if verify_phone == None:
                    return AjaxResponse().errorMessage(error="Wrong Phone number")
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)
           
           # view 层操作数据去update用户信息     
           try:
               user = User.objects.get(id=userid)
               user.set_password(password)
               user.save()

               User.objects.filter(id=userid).update(username=username,email=email,first_name=first_name,last_name=last_name,phone=phone)

               return AjaxResponse().successMessage("修改成功")
           except Exception as identifier:
               return AjaxResponse().errorMessage(error=identifier)

        else:
           return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")


def user_info(request) -> None:
    """ 用户信息修改 """
    if request.method == 'GET':
        if request.user.is_authenticated:
            userid = request.session['userid']
            # 通过用户ID获取用户信息，返回除了密码之外的数据
            try:
                user = User.objects.get(id=userid)
                data = {"username":user.username,
                        "email":user.email,
                        "phone":user.phone,
                        "last_name":user.last_name,
                        "firs_name":user.first_name}
                return AjaxResponse().successMessage(data=data)
            except Exception as identifier:
                return AjaxResponse().errorMessage(error=identifier)

        else:
            return AjaxResponse().errorMessage(error="User Not Login")
    else:
        return AjaxResponse().errorMessage(error="Method Allow POST")


def user_logout(request):
    logout(request)
    return AjaxResponse().successMessage()
