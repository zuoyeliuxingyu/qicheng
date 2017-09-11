from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group, Permission, ContentType
from django.http import JsonResponse, Http404
from django.db import IntegrityError
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "user/grouplist.html"
class GroupCreateView(View):
    def post(self, request):
        ret = {"status": 0}
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
class GroupUserList(LoginRequiredMixin, TemplateView):
    template_name = "user/group_userlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserList, self).get_context_data(**kwargs)
        # 将指定用户组内的成员列表取出来，然后传给模板
        gid = self.request.GET.get("gid", "")

        try:
            group_obj = Group.objects.get(id=gid)
            context['object_list'] = group_obj.user_set.all()
        except Group.DoesNotExist:
            raise Http404("group does not exist")
        context['gid'] = gid
        return context
class ModifyGroupPermissionList(TemplateView):
    template_name = "user/modify_group_permissions.html"

    def get_context_data(self, **kwargs):
        context = super(ModifyGroupPermissionList, self).get_context_data(**kwargs)
        context["contenttypes"] = ContentType.objects.all()
        context["group"] = self.request.GET.get("gid")
        context["group_permissions"] = self.get_group_permissions(context["group"])
        return context

    def get_group_permissions(self, groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")

    def post(self, request):
        permission_id_list = request.POST.getlist("permission", [])
        groupid = request.POST.get("groupid", 0)
        try:
            group_obj = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")

        if len(permission_id_list) > 0:
            permission_objs = Permission.objects.filter(id__in=permission_id_list)
            group_obj.permissions.set(permission_objs)
        else:
            group_obj.permissions.clear()
        return redirect("success", next="group_list")