# coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy


def index_test(request):
    # print(request)
    # print(request.path)
    # print(request.method)
    # print(request.META)
    # print(request.get_full_path())
    # return HttpResponse("Hello World!! 你好")

    """JsonResponse"""
    # ret = {"name": "reboot"}
    # ret_list = ["one", "two", "three", "four"]

    # JsonResponse 如果接受了 dict , 默认会进行 json 的序列化操作
    # return JsonResponse(ret)

    # 如果是 list，则需要将序列化参数设置为 False，默认为 True
    # return JsonResponse(ret_list, safe=False)

    """加载模板"""
    # t = loader.get_template("index.html")

    # context 就是往前端传递的内容，变量名就是字典的 key，必须以字典的格式传递
    context = {"name": "hello reboot!!!"}
    # return HttpResponse(t.render(context, request))
    # return render(request, "index.html", context)

    """简易用户登录"""
    if request.method == "POST":

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if username == "rock" and password == "123456":
            return HttpResponse("ok")
        else:
            return HttpResponse("faild")
    else:

        return render(request, "index.html")


def url_test(request, *args, **kwargs):
    """url 的位置参数和关键字参数"""
    print(args)
    print(kwargs)
    return HttpResponse("")

"""
@login_required
def index(request):
    return render(request, "index.html")
"""

class IndexView(LoginRequiredMixin ,TemplateView):
    template_name = "index.html"


class SuccessView(TemplateView):
    template_name = "public/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        success_name = self.kwargs.get("next", "")

        next_url = "/"
        try:
            next_url = reverse(success_name)
        except:
            pass

        context['next_url'] = next_url
        return context


class ErrorView(TemplateView):
    template_name = "public/error.html"

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        error_name = self.kwargs.get("next", "")
        errmsg = self.kwargs.get('msg', "")
        next_url = "/"
        try:
            next_url = reverse(error_name)
        except:
            pass
        context['next_url'] = next_url
        context['errmsg'] = errmsg
        return context