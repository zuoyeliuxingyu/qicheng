from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group
from django.http import JsonResponse, Http404
from django.db import IntegrityError

class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"

class GroupCreateView(View):
    def post(self,request):
        ret = {"status":0}
        group_name = request.POST.get("name","")
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
        return JsonResponse(ret,safe=True)

class GroupUserList(TemplateView):
    template_name = "user/group_userlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserList, self).get_context_data(**kwargs)
        # 将指定用户组内的成员列表取出来，然后传给模板
        gid = self.request.GET.get("gid","")
        try:
            group_obj = Group.objects.get(id=gid)
            context['object_list'] = group_obj.user_set.all()
        except Group.DoesNotExist:
            raise Http404
        context['gid'] = gid
        return context
