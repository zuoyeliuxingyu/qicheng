#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib.auth.models import User, Group
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict

class UserListView(LoginRequiredMixin, ListView):
    template_name = "accounts/userlist.html"
    model = User

    # ListView 封装好的分页器 每页几条数据
    paginate_by = 10

    # 最开始页码, 这里跟TemplateView 不一样就是paginator中的初始页面都是 +1
    initial_num = 1

    # 当前页显示几个页码
    display_num = 7
    # 当前页前面几个
    befor_num = 3
    # 当前页后面几个
    after_num = 3

    # 数据记录 操作
    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        # queryset = queryset.exclude(username="admin")  # 过滤用户不显示，比如普通用户不能看到admin用户
        queryset = queryset.exclude(is_superuser=True)  # 过滤用户不显示，比如普通用户不能看到admin用户

        username = self.request.GET.get("search_username", None)

        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context["page_range"] = self.get_pagerange(context["page_obj"])
        search_data = self.request.GET.copy()

        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context["search_data"] = "&" + search_data.urlencode()
        return context

    # 始终保持默认的页面数，搜索会有问题
    # def get_pagerange(self, page_obj):
    #     # 当前页
    #     current_index = page_obj.number
    #     # 总页数
    #     total_num = page_obj.paginator.num_pages
    #
    #     if total_num < self.display_num:
    #         start_num = self.initial_num
    #         end_num = self.display_num
    #     else:
    #         if current_index <= int(self.display_num/2):
    #             start_num = self.initial_num
    #             end_num = self.display_num
    #         else:
    #             start_num = current_index - self.befor_num
    #             end_num = current_index + self.after_num
    #             if (current_index + self.after_num) > total_num:
    #                 end_num = total_num
    #                 start_num = total_num - self.display_num + 1
    #     # 注意这里的结尾
    #     return range(start_num, end_num+1)


    def get_pagerange(self, page_obj):
        current_index = page_obj.number

        start = current_index -  self.befor_num
        end = current_index + self.after_num

        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages

        return range(start, end+1)

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
            ret["errmsg"] = "user dosen't exist."
        return JsonResponse(ret)


class ModifyUserGroupView(LoginRequiredMixin, View):
    def get(self, request):
        uid = request.GET.get("uid", "")
        group_obj = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:

            # 使用 models中的外键关系正向查找, 这里是过滤用户已在的组
            group_obj = group_obj.exclude(id__in=user_obj.groups.values_list("id"))
        return JsonResponse(list(group_obj.values("id", "name")), safe=False)

    def put(self, request):
        ret = {"status": 0}
        # django 默认只封装好了get 和post 的request数据 其他的需要自己用QueryDict 到request.body中取
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
            group_obj = Group.objects.get(id=gid)
            user_obj.groups.add(group_obj)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "user doesn't exist."
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "group doesn't exist."
        # 添加用户到指定组

        return JsonResponse(ret)

    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        gid = data.get("gid", "")
        uid = data.get("uid", "")
        try:
            user_object = User.objects.get(id=uid)
            group_object = Group.objects.get(id=gid)
            user_object.groups.remove(group_object)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "user doesn't exist."
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "user doesn't exist."
        return JsonResponse(ret)