from django.views.generic import ListView, View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, QueryDict


class UserListView(LoginRequiredMixin, ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 10
    ordering = "id" 

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()  # 存放列表对象(对应表里数据的集合)
        #queryset = queryset.exclude(username="admin")
        queryset = queryset.exclude(is_superuser=True)
        username = self.request.GET.get("search_username","")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        
        current_index = context["page_obj"].number
        before_page = current_index - 7
        after_page = current_index + 7

        context["page_range"] = self.get_pagerange(context["page_obj"])
        
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context['search_data'] = "&"+search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):

        current_index = page_obj.number
        before_page = current_index - 7
        after_page = current_index + 7

        if before_page <= 0:
            before_page = 1

        if after_page >= page_obj.paginator.num_pages:
            after_page = page_obj.paginator.num_pages

        return range(before_page, after_page + 1)

class ModifyUserStatus(View):

    def post(self, request):
        user_id = request.POST.get("uid", None)
        #print(user_id)
        ret={
            "status":0,
        }
        try:
            user_obj = User.objects.get(id=user_id)
            user_obj.is_active = False if user_obj.is_active else True
            user_obj.save()
        except User.DoesNotExist:
            ret["status"] = 1 
            ret["errmsg"] = "User is not exist!!!"
        return JsonResponse(ret)

class ModifyUserGroup(View):
    
    def get(self, request):
        uid = request.GET.get("uid", "")
        group_obj_s = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_obj_s.exclude(id__in=user_obj.groups.values_list("id")) # where id not in (1, 2, 3)
        return JsonResponse(list(group_obj_s.values("id", "name")),safe=False)

    def put(self, request):
        ret = {
            "status":0,
        }    
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        # print(data)

        try:
            user_obj = User.objects.get(pk=uid)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "User is not exist!"

        try:
            group_obj = Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "Group is not exist!"

        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

    def delete(self, request):
        ret = {
            "status": 0,
        }
        data = QueryDict(request.body)

        uid = data.get("uid", "")
        gid = data.get("gid", "")
        # print(data)

        try:
            user_obj = User.objects.get(pk=uid)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "User is not exist!"

        try:
            group_obj = Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "Group is not exist!"

        #1.通过用户删所在的组
        user_obj.groups.remove(group_obj)
        #2.通过组删除用户
        # group_obj.user_set.remove(user_obj)
        return JsonResponse(ret)


