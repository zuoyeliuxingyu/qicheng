from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

'''
@login_required
def index(request):
    #print(request)
    #print(request.scheme)
    #print(request.path)
    #print(request.method)
    #print(request.encoding)
    #print(request.META)
    #print(request.get_host())
    #print(request.get_port())
    #print(request.is_ajax())
    #return HttpResponse("Hello World!! 你好!")
    #ret = {"name": "reboot"}
    #ret_list = ["json", "python", "golang"]
    #return JsonResponse(ret_list, safe=False)
    #t = loader.get_template("test.html")
    #print(request.POST)
    #if request.method == "POST":
    #    username = request.POST.get("username", "")
    #    password = request.POST.get("password", "")
    #    if username == "wangjian" and password == "reboot":
    #        return HttpResponse("登录成功")
    #    else:
    #        return HttpResponse("登录失败")
    #else:
    #    return render(request,'test.html')
    return render(request,"public/index.html")
'''

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "public/index.html"

def userdetail(request, *args, **kwargs):
    print(args)
    print(kwargs)
    return HttpResponse("test")
