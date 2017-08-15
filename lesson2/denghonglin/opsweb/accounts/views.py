# coding:utf8
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView,View,ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage

# 作业 用户登陆与退出使用TemplateView与View去实现
# 用户登录class 视图
class LoginView(View):
    def get(self,request, *args, **kwargs):
        if request.method == "GET":
            return render(request,"public/login.html")

    def post(self,request, *args, **kwargs):
        if request.method == "POST":
            username = request.POST.get("username","")
            userpass = request.POST.get("password","")
            user = authenticate(username=username,password=userpass)
            ret = {"status":0, "errmsg":""}
            if user:
                login(request,user)
                ret['next_url'] = request.GET.get("next") if request.GET.get("next",None) else "/"
            else:
                ret["status"] = 1
                ret["errmsg"] = "用户名或密码错误，请联系管理员."
            return JsonResponse(ret)
            
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))
