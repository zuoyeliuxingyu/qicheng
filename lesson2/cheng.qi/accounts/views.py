from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator


# 用TemplateView 实现用户登录
class LoginTemplateView(TemplateView):
    template_name = "public/login.html"
    def get(self, request, *args, **kwargs):
        return super(LoginTemplateView, self).get(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        print(user)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)

# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("user_login"))

## 用templateView 实现用户退出
class LoginOutTemplateView(TemplateView):
    template_name = "public/login.html"
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))

def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username, user.email)
    return render(request, "user/userlist.html", {"userlist":user_queryset })

class User_ListView(View):
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()
        return render(request, "user/userlist.html", {"userlist": user_queryset})

#通过TemplateView实现分页的页码只显示15个记录， 显示当前页的前7个与后7个#
class UserListTemplateView(TemplateView):
    template_name = "user/userlist.html"
    per = 15

    def get_context_data(self, **kwargs):
        context = super(UserListTemplateView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1
        user_list = User.objects.all()
        paginator = Paginator(user_list, self.per)

        start_page_number = 1
        end_page_number = 16
        max_page_number = len(paginator.page_range)
#当点击page_num页大于7页时，显示当前页的前7页和当前页的后7页
        if page_num > 7:
            start_page_number = page_num - 7
            end_page_number = page_num + 8

# 当点击页是最后一页时，也显示15条数据#
        if end_page_number > max_page_number:
            start_page_number = max_page_number - 15
            end_page_number = max_page_number

        context["page_range"] = range(start_page_number, end_page_number)
        context["page_obj"] = paginator.page(page_num)
        context["object_list"] = context["page_obj"].object_list
        return context



class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("user_login"))
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
