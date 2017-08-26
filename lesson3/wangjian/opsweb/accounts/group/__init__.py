from django.views.generic import ListView,View
from django.contrib.auth.models import Group
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError
import traceback

class GroupListView(ListView):
    model = Group
    template_name = "user/grouplist.html"


class GroupCreateView(View):
    def post(self,request):
        ret = {"status":0}
        print(request.POST.get)
        group_name = request.POST.get("name","")
        if not group_name:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError:
            ret['stauts'] = 1
            ret['errmsg'] = "用户组以存在"
        """
        g = Group()
        g.name = group_name
        g.save()
        """

        return JsonResponse(ret)

# class GroupUserView(View):
#      def get(self,request):
#         print(request.GET)
#         gid = request.GET.get("gid","")
#         group = Group.objects.get(pk=gid)
#         users = group.user_set.all()
#         users_list = [{"username":user.name, "email": user.email, "id": user.id}for user in users]
#
#
#         return JsonResponse(users_list, safe=False)

# class GroupUserList(View):
#
#     def get(self, request):
#         gid = request.GET.get('gid', None)
#         ret = {"status":0}
#         print(request.GET)
#         if not gid:
#             ret['status'] = 1
#             ret['errmsg'] = 'gid不能为空'
#             return JsonResponse(ret, safe=False)
#         try:
#             group_obj = Group.objects.get(id=gid)               #获取指定组id的Group对象的object
#             users = group_obj.user_set.all()                    #获取指定组id对象的所有用户 <QuerySet [<User: wangjian>, <User: wangjian-5>, <User: wangjian-6>]>
#             users_list = list(users.values('id', 'username'))   #将QuerySet转化为list
#             ret['status'] = 0
#             ret['users_list'] = users_list
#             return JsonResponse(ret,safe=False)
#         except:
#             print(traceback.format_exc())
#             ret['status'] = 1
#             ret['errmsg'] = '查找组成员错误'
#             return JsonResponse(ret,safe=False)


class GroupUserList(View):
    def get(self, request):
        ret = {"status": 0}
        gid = request.GET.get('gid', "")
        if not gid:
            ret["status"] = 1
            ret["errmsg"] = "gid不能为空"
            return JsonResponse(ret, safe=False)
        try:
            group_obj = Group.objects.get(pk=gid)
            users = group_obj.user_set.all()
            users_list = list(users.values("id", "username"))
            ret['status'] = 0
            ret['users_list'] = users_list
            return JsonResponse(ret, safe=False)
        except:
            print(traceback.format_exc())
            ret['status'] = 1
            ret['errmsg'] = ''
            return JsonResponse(ret)