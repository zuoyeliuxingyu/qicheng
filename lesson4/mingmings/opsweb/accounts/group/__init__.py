#!/usr/bin/python
# coding=utf8
from django.contrib.auth.models import Group, User
from django.views.generic import View, TemplateView, ListView
from django.http import HttpResponse, JsonResponse, QueryDict, Http404
from django.db import IntegrityError


class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"


class GroupCreateView(View):
    """用户组创建视图"""
    def post(self, request):
        ret = {'status': 0}
        # print(request.POST)     # 一个 QueryDict
        group_name = request.POST.get("name", "")           # 获取 ajax 请求过来的变量

        if not group_name:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError:
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)


class GroupUserList(TemplateView):
    """用户组操作的逻辑"""
    template_name = 'user/group_userlist.html'

    def get_context_data(self, **kwargs):
        """用户组内的成员列表展示"""
        context = super(GroupUserList, self).get_context_data(**kwargs)

        gid = self.request.GET.get("gid", "")          # 获取前端传递的 gid
        try:
            group_obj = Group.objects.get(id=gid)       # 根据 gid 查询 group name
            '''
            get 会抛出两个异常
                - 取不到
                - 取到超过1条
            '''
            context['object_list'] = group_obj.user_set.all()   # 取出用户组内全部的用户对象
        except Group.DoesNotExist:
            raise Http404("用户组不存在")

        context['gid'] = gid
        return context


class GroupDeleteView(View):
    """删除 Group 的逻辑，响应前端 ajax 请求"""
    def post(self, request):
        ret = {'status': 0}
        group_id = request.POST.get('group_id', '')     # 获取前端 ajax 传递过来的 gid

        # 获取 idc_id 后进行对应的删除，异常给予报错提示
        try:
            group = Group.objects.get(id=group_id)
            group.delete()
        except Group.DoesNotExist:
            ret['stauts'] = 1
            ret['errmsg'] = "Group不存在"

        return JsonResponse(ret)
