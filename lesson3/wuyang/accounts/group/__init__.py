from django.views.generic import ListView, View,TemplateView
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.db import IntegrityError


class GroupListView(ListView):
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


# 展示指定组的所有用户列表
class GroupUserListView(TemplateView):
    template_name = "user/show_group_users.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserListView,self).get_context_data()
        group_id = kwargs["group_id"]
        try:
            group_obj = Group.objects.get(id=group_id)
        except Exception as e:
            print(e)
            group_obj=None

        if group_obj:
            user_list = group_obj.user_set.all() # 查询所有用户
            group_name = group_obj.name
            context["group_name"]=group_name
            context['user_list']=list(user_list.values("username","is_active"))
        return context




    def get(self, request, *args, **kwargs):
        group_id = request.GET.get("groupid")
        print(group_id)
        context = self.get_context_data(group_id=group_id)
        return self.render_to_response(context)


# 删除指定组的用户
class DelGroupUserView(View):
    def post(self,request):
        ret = {"status": 0}
        username = request.POST.get("username")
        groupname = request.POST.get("groupname")

        if username and groupname:
            try:
                user_object = User.objects.get(username=username)
                group_object = Group.objects.get(name=groupname)
                user_object.groups.remove(group_object)
                ret["status"]=0
            except Exception as e:
                print(e)
                ret["status"]=1
                ret["errmsg"]="用户组获取异常"
                return JsonResponse(ret)
        else:
            ret["status"]=1
            ret["errmsg"]="获取用户和组名失败"
        return JsonResponse(ret)


