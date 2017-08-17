from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import  View,TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
# -------------  以下为   函数视图  view类视图  templateview 类视图  三种方法 实现  login----------------
'''
def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)
'''


'''
# view 登录验证
class Login_View(View):

    def get(self,request,*args,**kwargs):
        return render(request, "public/login.html")
    

    def post(self,request,*args,**kwargs):
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)
'''



'''
TemplateView  的 template_name 指定 get 方法的模版名称
所以这个属性和 post 等其他属性无关
若有 其他方法还是要 自己去写相应的函数的。
'''
class LoginView(TemplateView):
    template_name = 'public/login.html'

    def get(self,request,*args,**kwargs):
        return  super(LoginView, self).get(request,*args,**kwargs)


    def post(self,request,*args,**kwargs):
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)


 # -------------  以下为   函数视图  view类视图  templateview 类视图  三种方法 实现  logout----------------
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("user_login"))

'''
# class view 实现退出
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return  HttpResponseRedirect(reverse("user_login"))
'''

#templateview 实现退出
class LogoutView(TemplateView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return  HttpResponseRedirect(reverse("user_login"))




# -------------  以下为   函数视图  view类视图  templateview 类视图  三种方法 实现  user_list----------------
@login_required
def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username, user.email)
    return render(request, "user/userlist.html", {"userlist":user_queryset })


# class UserListView(View):
#     @method_decorator(login_required)
#     def get(self,request,*args,**kwargs):
#         user_queryset = User.objects.all()
#         return render(request, "user/userlist.html", {"userlist": user_queryset})



'''
#---------------------------------------------------原始方法分页练习-------------------------------
class UserListView(TemplateView):
    template_name = 'user/userlist.html'
    per = 10

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserListView, self).get_context_data(**kwargs )
        try:
            page =  int(self.request.GET.get("page",1))
            print(page)
        except:
            page = 1

        start = (page - 1) * self.per
        end = page * self.per
        print(end ,start)
        context['userlist']=User.objects.all()[start:end]
        return context

'''

#---------------------------------------------------paginator  方法分页练习-------------------------------
class UserListView(TemplateView):
    template_name = 'user/userlist.html'
    per = 5

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserListView, self).get_context_data(**kwargs )
        try:
            page_num =  int(self.request.GET.get("page",1))
        except:
            page_num = 1


        user_list =  User.objects.all()
        paginator = Paginator(user_list,self.per)


        context['page_obj'] =  paginator.page(page_num)
        context['object_list'] = context['page_obj'].object_list

        showpage=15
        zong = paginator.num_pages
        current_page = context['page_obj'].number-1

        startpage = current_page - 7
        endpage = current_page + 8
        sdiffpage = 0
        ediffpage = 0

        if startpage < 0 :
            sdiffpage = -startpage

        if endpage > zong:
            ediffpage = endpage - zong

        endpage += sdiffpage
        startpage -= ediffpage

        if endpage > zong:
            endpage = zong
        if startpage < 0:
            startpage =0

        print(startpage,endpage)
        if zong > 15:
            context['page_range'] = paginator.page_range[startpage:endpage]

        return context

