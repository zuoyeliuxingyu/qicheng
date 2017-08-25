from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

'''
# 第一种登录验证
@login_required
def index(request):
        return render(request, "index.html")

# 第二种登录验证
class IndexView(TemplateView):
    template_name = 'index.html'

    # 使用登录验证装饰器
    @method_decorator(login_required)
    # 如果不使用登录验证装饰器，get方法就可以省略。
    def get(self, request, *arg, **kwargs):
        return super().get(request, *arg, **kwargs)
'''

# 第三种登录验证
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


#def userdetail(request, *args, **kwargs):
#    print(args)
#    print(kwargs)
#    return HttpResponse("")
