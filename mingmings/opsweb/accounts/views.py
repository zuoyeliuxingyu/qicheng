# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator


# Create your views here.
"""
def login_view(request):

    # 验证登录方法是否为 GET 方法
    if request.method == "GET":

        return render(request, "public/login.html")
    else:
        # 取用户名和密码
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        # 验证用户名和密码
        users = authenticate(username=username, password=password)
        ret = {"status":0, "errmsg":""}

        if users:
            # 调用 django 的 login 方法进行登录
            login(request, users)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            # 用户登录失败状态
            ret['status'] = 1
            ret['errmsg'] = "用户名和密码错误，请联系管理员"

        return JsonResponse(ret)


def logout_view(request):
    # 调用 django 自带 logout 方法退出
    logout(request)
    return HttpResponseRedirect(reverse_lazy('user_login'))


def user_list_view(request):

    user_queryset = User.objects.all()      # 查询所有用户
    for user in user_queryset:
        print(user.username, user.email)
    return render(request, "user/userlist.html", {"userlist": user_queryset})
"""

class LoginView(TemplateView):

    template_name = "public/login.html"

    def get(self, request, *args, **kwargs):
        """Template 自带的 get 方法"""
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request):
        """用户登录提交视图"""
        ret = {"status": 0}
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        # print(request.POST)
        # 对比数据库验证用户名和密码
        user = authenticate(username=username, password=password)

        # 验证成功返回的对象如果存在进行下一步动作
        if user is not None:

            # 判断用户是否状态是否为 active
            if user.is_active:
                login(request, user)

                # 向前端传递 next_url， 如果登录跳转到对应的页
                ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
                # return HttpResponse("用户登录成功")
            else:
                ret['status'] = 1
                ret['errmsg'] = "用户已禁用"
                # return HttpResponse("用户登录失败")
        else:
            ret['status'] = 2
            ret['errmsg'] = "密码错误"
            # return HttpResponse("用户登录失败")
        return JsonResponse(ret, safe=True)


class LogoutView(View):
    """登出视图"""

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponse("用户已退出")

"""
class User_ListView(View):
    '''用户管理类视图'''
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()      # 查询所有用户
        for user in user_queryset:
            print(user.username, user.email)
        return render(request, "user/userlist.html", {"userlist": user_queryset})


class User_TemplateView(TemplateView):
    """"""
    template_name = "user/userlist.html"
    per = 10

    def get_context_data(self, **kwargs):
        context = super(User_TemplateView, self).get_context_data(**kwargs)

        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1

        user_list = User.objects.all()
        paginator = Paginator(user_list, self.per)

        context['page_obj'] = paginator.page(page_num)
        context['object_list'] = context['page_obj'].object_list
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(User_TemplateView, self).get(request, *args, **kwargs)
"""