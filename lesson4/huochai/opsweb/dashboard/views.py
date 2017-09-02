from django.shortcuts import render, reverse

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

class SuccessView(TemplateView):
    template_name = 'public/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_name = self.kwargs.get('next')

        next_url = '/'
        try:
            next_url = reverse(success_name)
        except:
            pass
        context['next_url'] = next_url

        return context

class ErrorView(TemplateView):
    template_name = 'public/error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 打印关键字参数next
        print(self.kwargs)
        error_name = self.kwargs.get('next', '')
        #errmsg = self.kwargs.get('errmsg', '')

        next_url = "/"
        try:
            next_url = reverse(error_name)
        except:
            pass
        context['next_url'] = next_url
        #context['errmsg'] = errmsg
        print(context)
        return context
