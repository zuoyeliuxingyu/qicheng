from django.shortcuts import render, reverse

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

class SuccessView(TemplateView):
    template_name = "public/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        print(self.kwargs)
        success_name = self.kwargs.get("next")
        print(reverse(success_name))
        next_url = "/"
        try:
            next_url = reverse(success_name)
            context["next_url"] = reverse(success_name)
        except:
            pass
        return context

class ErrorView(TemplateView):
    template_name = "public/error.html"

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        print(self.kwargs)
        error_name = self.kwargs.get("next", "")
        errmsg = self.kwargs.get('msg', "")
        print(reverse(error_name))
        next_url = "/"
        try:
            next_url = reverse(error_name)
        except:
            pass
        context["next_url"] = next_url
        context["errmsg"] = errmsg
        return context