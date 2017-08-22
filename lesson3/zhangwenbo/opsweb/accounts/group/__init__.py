from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import render

class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"


class GroupCreateView(View):
    def post(self, request):
        ret = {"status":0}
        group_name = request.POST.get("name", "")
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
        """
        g = Group()
        g.name = group_name
        g.save()
        """
        return JsonResponse(ret)

class GroupuserListView(View):

    def get(self, request, *args, **kwargs):
        groupid = request.GET.get("gid", "")
        get_group = Group.objects.get(id=groupid)
        object_list = get_group.user_set.all()
        return render(request,"user/groupuserlist.html", {"object_list": object_list, "groupname":get_group})




