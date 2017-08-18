from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

# 函数视图定义登录
def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误"
        return JsonResponse(ret)

# 类视图定义登录
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "public/login.html")
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误"
        return JsonResponse(ret)

# 模板视图定义登录
class Login_View(TemplateView):
    template_name = 'public/login.html'
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        ret = {"status": 0, "errmsg": ""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误"
        return JsonResponse(ret)

# 函数视图定义退出
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))

# 类视图定义退出
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))

# 模板视图定义退出
class Logout_View(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))

# 通过视图函数获取用户数据
def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username, user.email)
    return render(request, 'user/userlist.html', {"userlist":user_queryset})

# 通过类视图获取用户数据
class User_ListView(View):
    #登录验证
    @method_decorator(login_required)
    #定义get方法
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()
        context = {'userlist':user_queryset}
        return render(request, 'user/userlist.html', context)

# 通过模板视图获取用户数据
class UserListView(TemplateView):
    template_name = 'user/userlist.html'
    per_page = 7
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1
        user_list = User.objects.all()
        paginator = Paginator(user_list, self.per_page)

        context['page_obj'] = paginator.page(page_num)
        context['object_list'] = context['page_obj'].object_list
        #print(context)
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)

# 自定义LoginRequiredMixin来理解该类的用途
class LoginRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        print('rock login')
        print(request.user)
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('user_login'))
        return super().dispatch(request, *args, **kwargs)
