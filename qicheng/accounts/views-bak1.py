from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
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

def logout_view(request):
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

# class UserListView(TemplateView):
#     template_name = "user/userlist.html"
#     before_index = 4
#     after_index = 3
#     # per = 15
#     def get_context_data(self, **kwargs):
#         context = super(UserListView, self).get_context_data(**kwargs)
        # try:
        #    page_num = int(self.request.GET.get("page", 1))
        # except:
        #    page_num = 1
        # user_list = User.objects.all()                  #获取所有用户列表对象#
        # paginator = Paginator(user_list,self.per)       #实例化Paginator#
        # context["page_obj"] = paginator.page(page_num)
        # context["object_list"] = context["page_obj"].object_list
        # return context

        # userlist = User.objects.all()  # 获取所有用户列表对象#
        # paginator = Paginator(userlist, 5)
        # page = self.request.GET.get("page", 1)   #获取当前第几页（页码数）
        # try:
        #     page_obj = paginator.page(page)     #获取当前页数据
        # except EmptyPage:
        #     page_obj = paginator.page(1)
        # context['page_obj'] = page_obj
        # #print page_obj
        # context['page_range'] = page_obj.paginator.page_range[page_obj.number - self.before_index: page_obj.number + self.after_index ]
        # return context




class UserListTemplateView(TemplateView):
    template_name = "user/userlist.html"
    per = 10

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
        if page_num > 7:
            start_page_number = page_num - 7
            end_page_number = page_num + 7

        if end_page_number > max_page_number:
            start_page_number = max_page_number - 15
            end_page_number = max_page_number

        context["page_range"] = range(start_page_number, end_page_number)
        context["page_obj"] = paginator.page(page_num)
        context["object_list"] = context["page_obj"].object_list

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)
    



class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("user_login"))
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
