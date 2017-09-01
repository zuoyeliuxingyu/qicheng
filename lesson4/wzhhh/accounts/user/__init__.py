from django.views.generic import ListView, View, DeleteView
from django.contrib.auth.models import User, Group
from accounts.views import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse, QueryDict

#Homework 3: Express limited pages
class UserListView(LoginRequiredMixin, ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 8
    scope = 7
    ordering = "id"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        """
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1

        user_list = User.objects.all()
        paginator = Paginator(user_list, self.paginate_by)
        start_page = page_num - self.scope  if page_num > self.scope else 1
        end_page = page_num + self.scope if page_num < paginator.num_pages - self.scope else paginator.num_pages
        context["page_obj"] = paginator.page(page_num)
        context["object_list"] = context["page_obj"].object_list
        context["page_range"] = range(start_page,end_page + 1)
        #edge of whether expressing "..."
        context["front_edge"] = self.scope + 1
        context["end_edge"] = paginator.num_pages - self.scope
        """

        page_num = context["page_obj"].number
        start_page = page_num - self.scope if page_num > self.scope else 1
        end_page = page_num + self.scope if page_num < context["paginator"].num_pages - self.scope else context["paginator"].num_pages
        context["page_range"] = range(start_page, end_page + 1)
        # edge of whether expressing "..."
        context["front_edge"] = self.scope + 1
        context["end_edge"] = context["paginator"].num_pages - self.scope

        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context["search_data"] = "&" + search_data.urlencode()
        return context

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()  #存放所有对象的集合，列表被重定义，每个元素是个对象
        #[<object>]
        queryset = queryset.filter(is_superuser = False)
        username = self.request.GET.get("search_username", None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

class ModifyUserStatusView(View):
    def post(self, request):
        uid = request.POST.get("uid", "")
        ret = {"status":0}
        try:
            user_obj = User.objects.get(id = uid)
            user_obj.is_active = False if user_obj.is_active else True
            user_obj.save()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"

        return JsonResponse(ret)


class ModifyUserGroupView(View):

    def get(self, request):
        print(request.GET)
        uid = request.GET.get("uid", "")
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in = user_obj.groups.values_list("id"))
        #select * from group where id not in( 1,2,3)
        return JsonResponse(list(group_objs.values("id", "name")), safe=False)

    def put(self, request):
        ret = {"status":0}
        print("request.GET: ", request.GET)
        print("request.POST: ", request.POST)
        print("QueryDict(request.body): ", QueryDict(request.body))
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] = 1
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

    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)#通过form表单传，在body体里
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
            group_obj = Group.objects.get(id=gid)
            group_obj.user_set.remove(user_obj)
            # user_obj.groups.remove(group_obj)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
        return JsonResponse(ret)