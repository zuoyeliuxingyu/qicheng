from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.core.paginator import Paginator


# 登录请求
def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        res = {"status": 0, "errmsg": ""}
        if user:
            login(request, user)
            res["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            res["status"] = 1
            res["errmsg"] = "用户名与密码错误,请联系管理员"
        return JsonResponse(res)

# 登录请求使用View 实现
class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, "public/login.html")

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            username = request.POST.get("username", "")
            userpass = request.POST.get("password", "")
            user = authenticate(username=username, password=userpass)
            res = {"status": 0, "errmsg": ""}
            if user:
                login(request, user)
                res["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
            else:
                res["status"] = 1
                res["errmsg"] = "用户名与密码错误,请联系管理员"
            return JsonResponse(res)


# 登出请求
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))

# 登出请求 View实现
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))

# 用户列表
def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username, user.email)
        return render(request, "user/userlist.html", {"userlist": user_queryset})

# 用户列表使用View实现
class UserListView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()
        return render(request, "user/userlist.html", {"userlist": user_queryset})

# 用户列表类
class UserListView(TemplateView):
    template_name = "user/userlist.html"
    per = 4
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1
        user_list = User.objects.all()
        paginator = Paginator(user_list, self.per)

        context["page_obj"] = paginator.page(page_num)
        context["object_list"] = context["page_obj"].object_list
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("user_login"))
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)