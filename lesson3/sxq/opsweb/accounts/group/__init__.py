from django.contrib.auth.models import Group
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError

class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"


class GroupCreateView(View):

    def post(self, request):
        ret = {"status":0}
        group_name = request.POST.get("name","")
        if not group_name:
            ret["status"] = 1
            ret["errmsg"] = "Group name is Null!!!"

        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError as e:
            ret["status"] = 1 
            ret["errmsg"] = "用户组已存在!!!"
        return JsonResponse(ret)

class GroupUserListView(TemplateView):
    template_name = "user/groupuserlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserListView, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            g = Group.objects.get(pk=gid)
        except:
            pass

        users = g.user_set.all()
        context['group_user_list'] = list(users.values("id", "username", "email"))
        context['gid'] = gid
        return context





