#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, Http404
from django.db import IntegrityError

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "accounts/grouplist.html"


class CreateGroupView(LoginRequiredMixin, View):
    def post(self, request):
        ret = {"status": 0}

        group_nmae = request.POST.get("name", "")
        group_nmae = request.POST.get('name', "")
        if not group_nmae:
            ret["status"] = 1
            ret["errmsg"] = "组名不能为空"
            return JsonResponse(ret)
        try:
            g = Group(name=group_nmae)
            g.save()
        except IntegrityError:
            ret["status"] = 1
            ret["errmsg"] = "用户组已存在"
        print(ret)
        return JsonResponse(ret)


# 就是处理几个gid传值
# class GroupUserListView(View):
#     @method_decorator(login_required)
#     def get(self, request, gid):
#         gid = gid
#         try:
#             group_obj = Group.objects.get(id=gid)
#         except Group.DoesNotExist:
#             group_obj = None
#
#         if group_obj:
#             user_obj = group_obj.user_set.all()
#         return render(request, "accounts/memberlist.html", {"user_obj": user_obj, "current_group": group_obj})


class GroupUserListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/group_userlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserListView, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
            # 只是利用models中的一对多关系的反向查询
            context["object_list"] = group_obj.user_set.all()
            context["group_boj"] = group_obj
        except Group.DoesNotExist:
            raise Http404("group does not exist.")
        context['gid'] = gid
        return context