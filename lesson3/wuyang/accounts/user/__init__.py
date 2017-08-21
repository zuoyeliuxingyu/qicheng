from django.views.generic import ListView, View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict

class UserListView(LoginRequiredMixin,ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 8
    before_range_num = 4
    after_range_num = 5


    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        queryset = queryset.filter(is_superuser=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        # 当前页  的前7条
        """
        current_index = context['page_obj'].number

        start = current_index - 3
        end = current_index + 3

        if start <= 0:
            start = 1

        if end > context['paginator'].num_pages:
            end = context['paginator'].num_pages


        context['page_range'] = range(start, end)
        """
        context['page_range'] = self.get_pagerange(context['page_obj'])
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end > page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end)


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
        print(request.GET)
        uid = request.GET.get('uid', "")
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))
        return JsonResponse(list(group_objs.values("id", "name")), safe=False)

    def put(self, request):
        ret = {"status":0}
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] =1
            ret['errmsg'] = "用户不存在"
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
            return JsonResponse(ret)
        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

