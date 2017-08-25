from django.views.generic import ListView, View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict

class UserListView(LoginRequiredMixin, ListView):
    template_name = 'user/userlist.html'
    model = User
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_superuser=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_index = context['page_obj'].number
        start = current_index - 3
        end = current_index + 4

        if start <= 0:
            start = 1

        if end > context['paginator'].num_pages:
            end = context['paginator'].num_pages

        context['page_range'] = range(start, end)
        print(context['page_range'])
        return context

class ModifyUserStatusView(View):
    def post(self, request):
        uid = request.POST.get("uid", "")
        ret = {"status":0}
        try:
            user_obj = User.objects.get(id=uid)
            #user_obj.is_active = False if user_obj.is_active else True
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True
            user_obj.save()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"

        return JsonResponse(ret)

class ModifyUserGroupView(View):
    def get(self, request):
        uid = request.GET.get("uid", "")
        group_objs = Group.objects.all()

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            # id__in 相当于 select * from group where id in (1,2,3,)
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))

        return JsonResponse(list(group_objs.values("id", "name")), safe = False)

    def put(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"

        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"

        user_obj.groups.add(group_obj)

        return JsonResponse(ret)

    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"

        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"

        user_obj.group.remove(grou_obj)

        return JsonResponse(ret)

