# coding:utf8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.base import View, TemplateView
from django.core.paginator import Paginator

# 登录验证方式 1
from django.contrib.auth.decorators import login_required, permission_required
# 登录验证方式 2
from django.utils.decorators import method_decorator

# Create your views here.


####################################################################   函数视图
#def login_view(request):
#
#    if request.method == "POST":
#
#        ret = {
#            "status":0,
#            "errmsg":"",
#        }
#        username = request.POST.get('username', "")
#        userpass = request.POST.get('userpass', "")
#
#        user = authenticate(username=username, password=userpass)
#        if user:
#            login(request, user)
#            ret["next_url"] = request.GET.get("next") if request.GET.get("next", "") else "/"
#        else:
#            ret["status"] = 1
#            ret["errmsg"] = "Login Fails!!!"
#        return JsonResponse(ret)
#    else:
#        return render(request, "public/login.html")
#
#def logout_view(request):
#    logout(request)
#    return HttpResponseRedirect(reverse("user_login"))

####################################################################   login/logout 使用 View 模板

#class LoginView(View):
#
#    def get(self, request, *args, **kwargs):
#        return render(request, "public/login.html")
#       
#    def post(self, *args, **kwargs): 
#        ret = {
#            "status":0,
#            "errmsg":"",
#        }
#        username = request.POST.get('username', "")
#        userpass = request.POST.get('userpass', "")
#
#        user = authenticate(username=username, password=userpass)
#        if user:
#            login(self.request, user)
#            ret["next_url"] = request.GET.get("next") if request.GET.get("next", "") else "/"
#        else:
#            ret["status"] = 1
#            ret["errmsg"] = "Login Fails!!!"
#        return JsonResponse(ret)

#class LogoutView(View):
#    def get(self, request, *args, **kwargs):
#        logout(request)
#        return HttpResponseRedirect(reverse("user_login"))
#
####################################################################   login/logout 使用 TemplateView 模板

class LoginView(TemplateView):

    template_name = "public/login.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
       return super(LoginView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        #context = super(LoginView, self).post(request, *args, **kwargs)
        ret = {
            "status":0,
            "errmsg":"",
        }
        if request.method == "POST":
            username = request.POST.get('username', "")
            userpass = request.POST.get('userpass', "")

            user = authenticate(username=username, password=userpass)
            if user:
                login(request, user)
                ret["next_url"] = request.GET.get("next") if request.GET.get("next", "") else "/"
            else:
                ret["status"] = 1
                ret["errmsg"] = "Login Fails!!!"

            return JsonResponse(ret)


class LogoutView(TemplateView): 

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))


####################################################################   分页 ，每页显示15个分页标签
 

# 使用View 模板展现用户列表
#class UserListView(View):
#    def get(self, *args, **kwargs):
#        user_list = User.objects.all()
#        return render(self.request, "user/userlist.html", {"userlist":user_list})


# 使用TemplateView 模板展现用户列表
class UserListView(TemplateView):
    template_name = "user/userlist.html"
    per = 5
    before_num = 7 
    after_num = 7 

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1

        userlist = User.objects.all()
        paginator = Paginator(userlist, self.per)
        nonce_page = paginator.page(page_num)

        #count_page = paginator.num_pages  

        if nonce_page.number - self.before_num <= 0:
            self.before_num = 0
        else:
            self.before_num = nonce_page.number - self.before_num

        if nonce_page.number + self.before_num >= paginator.num_pages:
            self.after_num = paginator.num_pages
        else:
            self.after_num = nonce_page.number + self.after_num

        #print(range(self.before_num,self.after_num))

        context["page_range"]=range(self.before_num+1,self.after_num+1) 
        context["page_obj"] = paginator.page(page_num)
        context["object_list"] = context["page_obj"].object_list

        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
       return super(UserListView, self).get(request, *args, **kwargs)


####################################################################   django 1.11.x 登录验证方式 3

#class LoginRequiredMixin(object):
#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authentircated():
#            return HttpResponseRedirect(reverse("user_login")) 
#        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
