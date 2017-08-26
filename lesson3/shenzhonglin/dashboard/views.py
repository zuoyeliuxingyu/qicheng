from django.shortcuts import render

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# LoginRequiredMixin django 一种验证方式
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"