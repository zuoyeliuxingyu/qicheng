from django.shortcuts import render

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
# django default auth model
from django.contrib.auth import logout, login, authenticate
# django default User model
from django.contrib.auth.models import User
# django base View ,if you use class view
from django.views.generic import View
# class view auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# class TemplateVie view
from django.views.generic import TemplateView
# django Paginator
from django.core.paginator import Paginator


def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user_obj = authenticate(username=username, password=password)
        ret = {"status":0, "errmsg": ""}
        if user_obj:
            login(request,user_obj)
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "user or password error or user if not Active..."
        return JsonResponse(ret)

# login base View come true
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "public/login.html")
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = authenticate(username=username, password=password)
        ret = {"status":0, "errmsg": ""}
        if user_obj:
            login(request, user_obj)
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "user or password error or user if not Active..."
        return JsonResponse(ret)

# login TemplateView come true
class LoginView(TemplateView):
    template_name = "public/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = authenticate(username=username, password=password)
        ret = {"status":0, "errmsg": ""}
        if user_obj:
            login(request, user_obj)
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"]  = "username orr passowrd error or user if not Active..."
        return JsonResponse(ret)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))

# logout base View come true
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))

# logout TemplateView come true
class LogoutView(TemplateView):
    get_redirect_url = "user_login"

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))
    

def user_list_view(request):
    user_obj = User.objects.all()
    return render(request, "accounts/userlist.html", {"userlist": user_obj})

class UserListView(View):
    @method_decorator(login_required) # 类视图认证
    def get(self, request, *args, **kwargs):
        user_obj = User.objects.all()
        return render(request, "accounts/userlist.html", {"userlist": user_obj})

class UserListView(TemplateView):
    template_name = "accounts/userlist.html"
    per_num = 10

    def get_context_data(self, **kwargs):
        context = super(UserListView,self).get_context_data(**kwargs)

        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1

        user_obj = User.objects.all()
        paginator = Paginator(user_obj, self.per_num)

        '''
            思路：
            如果 总页数 < 显示页数：
                开始索引 = 0        # 为什么是0 看 paginator page_range 源码
                结束索引 = 显示页数
            否则  # 也就是说 总页数 >= 显示页数：
                如果 当前页 <= 显示页数的1/2：
                    开始索引 = 0
                    结束索引 = 显示页数
                否则：# 也就是说 总页数 >= 显示页数： 并且 当前页 > 显示页数的1/2
                    开始索引 = 当前页 - 前面显示页数
                    结束索引 = 当前页 + 后面显示页数
                    如果：当前页 + 后面显示页数 > 总页数：
                        结束索引 = 总页数
                        开始索引 = 总页数 - 显示页数 # 最后还是有 15页数
        '''

        # 最开始页数
        initial_num = 0
        # 当前页前面的 页数 为什么是8 django Paginator 实例化对象
        # page_range 源码表示从1开始也就是说 当前 数 + 1 end index 默认也+1
        '''
            def page_range(self):
            """
            Returns a 1-based range of pages for iterating through within
            a template for loop.
            """
            return six.moves.range(1, self.num_pages + 1)
        '''
        befort_num = 8
        # 当前页后面 的页数
        after_num = 7
        # 每页显示15 页数
        display_num = 15

        # 借用 paginator 对象中 的 总页数
        total_num = paginator.num_pages

        if total_num < display_num:
            start_num = initial_num
            end_num = display_num
        else:
            if page_num <= int(display_num/2):
                start_num = initial_num
                end_num = display_num
            else:
                start_num = page_num - befort_num
                end_num = page_num + after_num
                if (page_num + befort_num) > total_num:
                    end_num = total_num
                    start_num = total_num - display_num

        page_range = paginator.page_range[start_num:end_num]

        context["page_obj"] = paginator.page(page_num)
        context["object_list"] = context["page_obj"].object_list
        context["page_rang"] = page_range

        return context

    @method_decorator(login_required) # TemplateView 类视图认证
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)