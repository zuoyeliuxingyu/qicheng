from django.views.generic import View, ListView, CreateView
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.db import IntegrityError

class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"

class GroupUserListView(ListView):
    model = Group
    template_name = "user/groupuserlist.html"

    def get_queryset(self):
        print(self.request.GET)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            pass
        else:
            user_objs = group_obj.user_set.all()
        queryset = user_objs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupUserListView, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            pass
        else:
            context["group_obj"] = group_obj
        return context

'''
class GroupCreateView(View):
    def post(self, request):
        ret = {"status":0}
        groupname = request.POST.get("name", "")
        if not groupname:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        print(request.POST)
        try:
            """
            g = Group()
            g.name = groupname
            g.save()
            """
            g = Group(name=groupname)
            g.save()
        except IntegrityError as e:
            print("IntegrityError")
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)
'''
class GroupCreateView(CreateView):

    def post(self, request):
        ret = {"status":0}
        groupname = request.POST.get("name", "")
        if not groupname:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        print(request.POST)
        try:
            """
            g = Group()
            g.name = groupname
            g.save()
            """
            g = Group(name=groupname)
            g.save()
        except IntegrityError as e:
            print("IntegrityError")
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)