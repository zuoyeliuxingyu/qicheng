#!/usr/bin/env python
# -*- coding:utf-8 -*-

# import view model
from django.views.generic import View, TemplateView, ListView
# import User Group model
from django.contrib.auth.models import User, Group
# import auth model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse, QueryDict

class UserListView(LoginRequiredMixin, ListView):
    template_name = "accounts/userlist.html"
    model = User
    paginate_by = 10

    # 最开始页数
    initial_num = 1

    # 每页几个
    display_num = 15

    before_num = 7
    after_num = 8

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context["page_range"]  = self.get_pagerange(context["page_obj"])
        return context

    def get_pagerange(self, page_obj):
        # 当前页
        current_index = page_obj.number
        # 总页数
        total_num = page_obj.paginator.num_pages

        if total_num < self.paginate_by:
            start = self.initial_num
            end = self.paginate_by
        else:
            if current_index <= int(self.display_num/2):
                start = self.initial_num
                end = self.display_num + 1
            else:
                start = current_index - self.before_num
                end = current_index + self.after_num
                if (current_index + self.before_num) > total_num:
                    end = total_num
                    start = total_num - self.display_num
        return range(start, end)

class ModifyUserStatusView(LoginRequiredMixin, View):
    def post(self, request):
        uid = request.POST.get("uid", "")
        ret = {"status": 0}
        try:
            user_obj = User.objects.get(id=uid)
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True
            user_obj.save()
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "user dosen't exist"
        return JsonResponse(ret)

class ModifyUserGroupView(View):
    def get(self, request):
        uid = request.GET.get('uid', "")
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))
        return JsonResponse(list(group_objs.values("id", "name")), safe=False)

    def put(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "user dosen't exist"
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "group dosen't exist"
            return JsonResponse(ret)
        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        gid = data.get("gid")
        uid = data.get("uid")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "user dosen't exist"
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret["status]"] = 1
            ret["errmsg"] = "group dosen't exist"
        user_obj.groups.remove(group_obj)

        return JsonResponse(ret)
