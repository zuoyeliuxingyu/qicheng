#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse

class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "public/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)

        success_name = self.kwargs.get("next", "")

        next_url = "/"
        try:
            next_url = reverse(success_name)
        except:
            pass
        context["next_url"] = next_url
        return context

class ErrorView(LoginRequiredMixin, TemplateView):
    template_name = "public/error.html"

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)

        error_name = self.kwargs.get("next", "")
        errmsg = self.kwargs.get("msg", "")
        next_url = "/"
        try:
            next_url = reverse(error_name)
        except:
            pass
        context["next_url"] = next_url
        context["errmsg"] = errmsg
        return context