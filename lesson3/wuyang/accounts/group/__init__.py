from django.views.generic import ListView, View
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.db import IntegrityError
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


