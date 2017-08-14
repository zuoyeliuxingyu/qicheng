from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.core.paginator import Paginator

# 类视图登录验证
from django.utils.decorators import method_decorator


########################### 函数视图 #################################
#def login_view(request):
#    if request.method == 'POST':
#        username = request.POST.get('username',"")
#        userpass = request.POST.get('userpass',"")
#        ret = {
#            "status":0,
#            "errmsg":"",
#        }
#        # 验证用户，用户或密码错误验证为空；新版本中用户被禁用，认证结果也会为空
#        user = authenticate(username=username, password=userpass) 
#        if user: 
#            login(request, user)
#            ret["next_url"] = request.GET.get("next") if request.GET.get('next', None) else "/"
#        else:
#            ret["status"] = 1
#            ret["errmsg"] = "User don't exist or Password is Wrong or User disabled!!!"
#        return JsonResponse(ret)
#    else:
#        return render(request, "public/login.html")
#    
#def logout_view(request):
#    logout(request)
#    return HttpResponseRedirect(reverse("user_login"))
#
#def user_list_view(request):
#    user_queryset = User.objects.all() 
#    return render(request, 'user/userlist.html', {"user_list": user_queryset})


######################################################## 类视图 # View 模板

#class LoginView(View):
#
#    def get(self, request, *args, **kwargs):
#        return render(request, "public/login.html")
#
#    def post(self, request, *args, **kwargs):
#        username = request.POST.get('username',"")
#        userpass = request.POST.get('userpass',"")
#        ret = {
#            "status":0,
#            "errmsg":"",
#        }
#        # 验证用户，用户或密码错误验证为空；新版本中用户被禁用，认证结果也会为空
#        user = authenticate(username=username, password=userpass)
#        if user:
#            login(request, user)
#            ret["next_url"] = request.GET.get("next") if request.GET.get('next', None) else "/"
#        else:
#            ret["status"] = 1
#            ret["errmsg"] = "User don't exist or Password is Wrong or User disabled!!!"
#        return JsonResponse(ret)

#class LogoutView(View):
#
#    def get(self, request, *args, **kwargs):
#        logout(self.request)
#        return HttpResponseRedirect(reverse("user_login"))

######################################################## 类视图 # TemplateView 模板

class LoginView(TemplateView):
    template_name = "public/login.html"
    
    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        ret = {
            "status":0,
            "errmsg":"",
        }
        if request.method == "POST":
            username = request.POST.get('username',"")
            userpass = request.POST.get('userpass',"")
            user = authenticate(username=username, password=userpass)

            if user:
                login(request, user)
                ret["next_url"] = request.GET.get("next") if request.GET.get('next', None) else "/"
            else:
                ret["status"] = 1
                ret["errmsg"] = "Login Fails!!!"
            return JsonResponse(ret)
        
class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))


######################################################## 类视图 # View/ TemplateView

#class User_ListView(View):
#
#    @method_decorator(login_required)
#    def get(self, request, *args, **kwargs):
#        user_queryset = User.objects.all()
#        return render(request, 'user/userlist.html', {"user_list": user_queryset}) 


#class UserListView(TemplateView):
#
#    # TemplateView 继承了 TemplateResponseMixin，template_name 就是TemplateResponseMixin 里的属性
#    template_name = "user/userlist.html"
#
#    per = 10
#
#    def get_context_data(self, **kwargs):
#        context = super(UserListView, self).get_context_data(**kwargs)
#        try:
#            page_num = int(self.request.GET.get('page',1))
#        except:
#            page_num = 1
#
#        end_num = page_num * self.per
#        start_num = end_num - self.per
#
#        context["user_list"] = User.objects.all()[start_num:end_num]
#        return context


class UserListView(TemplateView):

    template_name = "user/userlist.html"
    per = 3
    before_page = 7 
    after_page = 7 
    
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get('page',1))
        except:
            page_num = 1

        user_list = User.objects.all()
        paginator = Paginator(user_list, self.per)
        
        nonce_page = paginator.page(page_num).number
        
        if nonce_page - self.before_page <= 0:
            self.before_page = 1
        else:
            self.before_page = nonce_page - self.before_page

        if nonce_page + self.after_page >= paginator.num_pages:
            self.after_page = paginator.num_pages
        elif nonce_page + self.after_page < 15:
            self.after_page = 15
        else:
            self.after_page = nonce_page + self.after_page


        context['page_range'] = range(self.before_page,self.after_page+1)
        context['page_obj'] = paginator.page(page_num)
        context['object_list'] = context['page_obj'].object_list

        return context
        
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)


######################################################## 类视图 # 登录验证

#class LoginRequiredMixin(object):
#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authentircated():
#            return HttpResponseRedirect(reverse("user_login"))
#        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
