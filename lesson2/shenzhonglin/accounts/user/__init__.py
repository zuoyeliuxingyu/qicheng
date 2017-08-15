#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class UserListView(LoginRequiredMixin, ListView):
    template_name = "accounts/userlist.html"
    model = User
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["userlist"] = User.objects.all()
    #     return context

    # paginate_by = 6 # 分页中的每页几条数据