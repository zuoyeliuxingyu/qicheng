from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View,TemplateView         #django视图 View 和模板视图
from django.utils.decorators import method_decorator       #类视图验证的方法
from django.contrib.auth.decorators import login_required  #类视图验证的方法
from django.core.paginator import Paginator, EmptyPage

# Create your views here.

'''
 # 练习的登录函数视图 login_view  和 logout_view
 
# def login_view(request):
#     if request.method == "GET":
#         return render(request, "public/login.html")
#     else:
#         print(request.POST)
#         username = request.POST.get("username", "")
#         password = request.POST.get("password", "")
#         user = authenticate(username=username, password=password)
#         ret = {"status": 0, "errmsg": ""}
#         if user:
#             #用户名与密码是正确的
#                 #用户可以登录
#             login(request, user)
#             ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
#         else:
#             ret['status'] = 1
#             ret['errmsg'] = "用户名或密码错误，请联系管理员"
#             #用户名或密码不正确
#         return JsonResponse(ret)

# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("user_login"))

'''

class LoginView(View):           #LoginView类视图
    def get(self, request, *args, **kwargs):

        return render(request, "public/login.html")

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
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)

class LogoutView(View):           #LogoutView 类视图
    def get(self,request,*args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))

class LoginTemplateView(TemplateView):       #Login 基于TemplateView视图
    template_name = "public/login.html"

    def get(self,request,*args,**kwargs):
        context = super(LoginTemplateView, self).get(**kwargs)
        return context

    def post(self,request,*args,**kwargs):
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        user = authenticate(username=username,password=password)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request,user)
            ret['next_url'] = request.GET.get('next') if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)

class LogoutTemplateView(TemplateView):       #Logout 基于TemplateView视图
    template_name = "public/login.html"
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))




def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username, user.email)
    #return HttpResponse("")
    return render(request, "user/userlist.html", {"userlist":user_queryset})



#路由功能 抛出异常 get请求就路由到get方法 post请求就路由到post方法

class User_ListView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()
        return render(request,"user/userlist.html",{"userlist": user_queryset})

"""
class UserListView(TemplateView):
    template_name = "user/userlist.html"   #TemplateView 继承的TemplateResponseMixin类  template_name 是TemplateResponseMixin的属性
    per = 5

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs) #context先继承父类的方法
          #context['userlist'] 是要传给前端userlist.html的数据
        # try:
        #     page = int(self.request.GET.get("page",1))
        # except:
        #     page = 1
        #
        # end = self.per * page
        # start = end - self.per
        #
        # context["userlist"] = User.objects.all()[start:end]
        #
        # return context
        try:
            page_num = int(self.request.GET.get("page",1))         #获取当前的页面number
        except:
            page_num = 1

        userlist = User.objects.all()                              #获取所有要展示的数据userlist
        paginator = Paginator(userlist, self.per)                  #要展示的所有数据进行分页实例化   按每页10条进行分页
        context['page_obj'] = paginator.page(page_num)             #传入模板内 分页的对象
        context['object_list'] = context['page_obj'].object_list   #传入模板内 实际要展示的数据对象

        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)

"""