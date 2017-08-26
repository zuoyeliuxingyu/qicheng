#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "accounts/grouplist.html"

class GroupCreateView(LoginRequiredMixin, View):
    def post(self, request):
        ret = {"status": 0}
        groupname = request.POST.get('name')

        if groupname:
            try:
                group_obj = Group()
                group_obj.name = groupname
                group_obj.save()
            except:
                ret["status"] = 1
                ret["errmsg"] = "create group fail.."
        return JsonResponse(ret)


class GroupUserView(View):

    @method_decorator(login_required)
    def get(self, request, gid):
        gid = gid
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            group_obj = None

        if group_obj:
            user_obj = group_obj.user_set.all()

        return render(request, "accounts/memberlist.html", {"user_obj": user_obj, "current_group": group_obj})

