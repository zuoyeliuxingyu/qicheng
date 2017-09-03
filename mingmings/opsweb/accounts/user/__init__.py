# coding=utf-8
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse, QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin ,ListView):
    """用户展示视图"""

    template_name = "user/userlist.html"
    model = User
    paginate_by = 10        # 每页展示多少对象
    before_index = 7        # 当前页往前几页
    after_index = 7         # 当前页往后几页

    def get_queryset(self):
        """查询数据库，获得查询对象的集合，list，其中每个元素对应数据表里的一条记录"""
        queryset = super(UserListView, self).get_queryset()
        # queryset = queryset.exclude(username="admin")           # 过滤掉 username=admin 的 用户，排除超级管理员
        # queryset = queryset.exclude(is_superuser=True)           # 过滤掉有 is_superuser  属性的用户，排除超级管理员
        queryset = queryset.filter(is_superuser=False)           # 过滤掉有 is_superuser  属性的用户

        username = self.request.GET.get("search_username", "")     # 查询前端传递的 username
        if username:
            queryset = queryset.filter(username__icontains=username)    # 按用户名搜索

        return queryset


    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)  # 覆盖父类的属性

        # 向前端传递的变量
        context['page_range'] = self.get_page_range(context['page_obj'])    # 可以循环的 page 对象
        context['users'] = User.objects.all()   # 所有的 user 对象

        """
        原本往前端传递一个自定义变量通过 context[xxx] = xxx 往字典里增添一对 k,v 即可在前端通过 {{ xxx }} 调用
        但是当需要往前端传递多个自定义变量的时候通过这种定义显得非常丑陋并且不实用。又因这些 k,v 保存在 QueryDict 的字典中，
        所以把这个字典添加到 context 这个字典里即可
        print(self.request.GET)
        <QueryDict: {u'hostname': [u'fang']}>

        print(self.request.GET.dict())
        {u'hostname': [u'fang']}
        """
        context.update(self.request.GET.dict())

        # 处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop["page"]
        except:
            pass

        context.update(search_data.dict())
        context['search_data'] = "&"+search_data.urlencode()

        return context

    def get_page_range(self, page_obj):
        """
        分页处理逻辑
            page_obj 是需要传递的参数，为当前页的模型对象，可以通过遍历的方式得到该对象里的内容

        处理思路：
            - 能够让用户循环的全部 user 的 list，称之为外部 list
            - 最终展示的页码的集合一定是这个外部 list 内的一个更小的 list，是上述外部 list 的子集
        """

        # 开始序列号 = 当前页码号 - 后置序列号
        start_index = page_obj.number - self.before_index

        # 应对开始序列异常的情况，最小不能为 0
        if start_index < 0:
            start_index = 0

        # 最终在页面上供展示的循环的 list
        page_range = page_obj.paginator.page_range[start_index: page_obj.number + self.after_index]
        return page_range


class ModifyUserStatusView(View):
    """响应后端 ajax 请求修改用户状态的逻辑"""

    def post(self, request):
        ret = {'status': 0}
        uid = request.POST.get('uid', "")
        try:
            user_obj = User.objects.get(pk=uid)

            # 这里注意一旦前端点击按钮，将会修改 is_active 状态，所以修改的值和用户的 is_active 是相反的
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True

            user_obj.save()     # 保存到 DB
        except User.DoesNotExist:
            ret['stauts'] = 1
            ret['errmsg'] = "用户不存在"

        return JsonResponse(ret, safe=True)


class ModifyUserGroupView(View):
    """修改用户和组关系的逻辑"""

    def get(self, request):
        """展示用户组列表"""
        print(request.GET)
        uid = request.GET.get('uid', '')
        group_objs = Group.objects.all()

        try:
            user_obj = User.objects.get(id=uid)

        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))

        return JsonResponse(list(group_objs.values("id", "name")), safe=False)

    def put(self, request):
        """将用户加入到用户组逻辑"""
        ret = {"status": 0}
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
            group_obj = Group.objects.get(id=uid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
            return JsonResponse(ret)

        # 将用户添加到用户组
        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        try:
            user_obj = User.objects.get(id=data.get("uid", ""))
            group_obj = Group.objects.get(id=data.get("gid", ""))
            user_obj.groups.remove(group_obj)
            # group_obj.user_set.remove(user_obj)
        except User.DoesNotExist:
            ret["status"] = 1
            ret['errmsg'] = "用户不存在"
        except Group.DoesNotExist:
            ret["status"] = 1
            ret['errmsg'] = "用户组不存在"

        return JsonResponse(ret)
