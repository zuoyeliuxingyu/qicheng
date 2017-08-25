from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponse, QueryDict
from django.db import IntegrityError

class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"

class GroupCreateView(View):
    def post(self, request):
        ret = {'status': 0}
        group_name = request.POST.get("name","")
        if not group_name:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse
        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError:
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)

class GroupGnameView(TemplateView):
    template_name = "user/groupname.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            gname = context['groupname']
            groupqueryset = Group.objects.get(name=gname)
            userqueryset = groupqueryset.user_set.all()
            context['object_list'] = userqueryset
        except Group.DoesNotExist:
            pass

        return context

