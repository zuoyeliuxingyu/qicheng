from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse,HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = authenticate(username=username, password=password)
        ret = {"status": 0}
        if user_obj:
            login(request, user_obj)
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None)  else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "username or password error or user is not active"
        return JsonResponse(ret)


class UserLoginView(View):
    def get(self, request):
        return render(request, "public/login.html")

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user_obj = authenticate(username=username, password=password)
        ret = {"status": 0}
        if user_obj:
            login(request, user_obj)
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "username or password error or user is not active."
        return JsonResponse(ret)


class UserLoginView(TemplateView):
    template_name = "public/login.html"

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user_obj = authenticate(username=username, password=password)
        ret = {"status": 0}
        if user_obj:
            login(request, user_obj)
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "username or password error or user is not active."
        return JsonResponse(ret)


def logout_view(request):
    logout(request)
    # return HttpResponseRedirect(reverse("user_login"))
    return redirect("user_login")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("user_login")


class UserLogoutView(TemplateView):
    template_name = "public/login.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("user_login")


class UserListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/userlist.html"

    # 每页10条数据
    per = 10

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1

        user_obj = User.objects.all()
        # 实例化 paginator对象 并且将user_obj 和 数据条数作为 参数传值
        paginator = Paginator(user_obj, self.per)

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

        # 最开始页
        initial_num = 0

        # 当前页前面的页数
        befort_num = 4

        # 当前页后面的页数
        after_num = 3

        # 每页显示的页码数
        display_num = 7

        # 借用paginator 对象中的中页数
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

        page_range = paginator.page_range[start_num: end_num]

        context["page_obj"] = paginator.page(page_num)
        # 当前分页对象的元素列表
        context["object_list"] = context["page_obj"].object_list

        # context["page_range"] = paginator.page_range
        context["page_range"] = page_range
        print(paginator.page_range, 'page_range')
        return context