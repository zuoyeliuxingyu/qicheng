from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
#@login_required
#def index(request):
#    return render(request, 'index.html')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

   # @method_decorator(login_required)
    #def get(self, request, *args, **kwargs):
    #    return super(IndexView, self).get(request, *args, **kwargs)

def user_details(request, *args, **kwargs):
    print(args)
    print(kwargs)
    return HttpResponse("hello")
