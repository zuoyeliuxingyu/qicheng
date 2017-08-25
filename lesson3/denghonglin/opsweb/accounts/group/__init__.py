from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group,User
from django.http import JsonResponse, HttpResponse,QueryDict
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

class ShowUserGroupView(TemplateView):
    template_name = "user/group_users.html"

    def get_context_data(self, **kwargs):
        context = super(ShowUserGroupView,self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid","")
        try:
            group = Group.objects.get(id=gid)
        except:
            return HttpResponse("用户组不存在")

        context['group_users'] = group.user_set.all()
        context['groupname'] = group
        return context

class DelGroupUser(View):
    def delete_group_user(self,request):
        ret = {"status":0}
        data = QueryDict(request.body)
        uid = data.get('userid',"")
        gid = data.get('groupid',"")
        print(gid)
        print(uid)
        try:
            user = User.objects.get(id=uid)
            group = Group.objects.get(id=gid)
            group.user_set.remove(user)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"

        return JsonResponse(ret,safe=True)






