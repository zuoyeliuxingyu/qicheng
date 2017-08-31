from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):
    return render(request, "index.html")


class IndexView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "index.html")


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"