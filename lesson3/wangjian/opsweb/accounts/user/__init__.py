from django.views.generic import ListView,TemplateView,View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse,QueryDict


class UserListView(ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 10  # 每页展示多少个数据
    before_range_num = 7  # 当前页往前多少页
    after_range_num = 7  # 当前页往后多少页

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset() #返回查询集，model 定义的user表里的查询的数据
        queryset = queryset.filter(is_superuser=False)      #filter过滤is_superuser=False的非管理员用户
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

    def get_pagerange(self, page_obj):                      #分页代码做页码运算逻辑#
        current_index = page_obj.number                     #赋值给当前页的变量
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end > page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages

        return range(start, end)

"""
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)   #基础父类属性

        #在给前端进行传递的变量
        context['page_range'] = self.get_page_range(context['page_obj']) #可以循环的page对象
        context['users'] = User.objects.all()    #所有 user对象

        
        原本往前端传递一个自定义变量通过 context[xxx] = xxx 往字典里增添一对 k,v 即可在前端通过 {{ xxx }} 调用
        但是当需要往前端传递多个自定义变量的时候通过这种定义显得非常丑陋并且不实用。又因这些 k,v 保存在 QueryDict 的字典中，
        所以把这个字典添加到 context 这个字典里即可
        print(self.request.GET)
        <QueryDict: {u'hostname': [u'fang']}>

        print(self.request.GET.dict())
        {u'hostname': [u'fang']}
        

        context.update(self.request.GET.dict())
        return context

def get_page_range(self, page_obj):
    
    分页处理逻辑
        page_obj 是需要传递的参数，为当前页的模型对象，可以通过遍历的方式得到该对象里的内容

    处理思路：
        - 能够让用户循环的全部 user 的 list，称之为外部 list
        -  最终展示的页码的集合一定是这个外部 list 内的一个更小的 list，是上述外部 list 的子集
    

    # 开始序列号 = 当前页码号 - 后置序列号
    start_index = page_obj.number - self.before_index

    # 应对开始序列异常的情况，最小不能为 0
    if start_index < 0:
        start_index = 0

    # 最终在页面上供展示的循环的 list
    page_range = page_obj.paginator.page_range[start_index: page_obj.number + self.after_index]
    return page_range
"""


class ModifyUserStatusView(View):    #修改用户状态(禁用，开启)的类视图逻辑
    def post(self,request):
        uid = request.POST.get('uid',"")
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


class ModifyUserGroupView(View):                    #修改用户所在组视图

    def get(self, request):
        print(request.GET)
        uid = request.GET.get("uid","")

        group_objs = Group.objects.all()

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))

        return JsonResponse(list(group_objs.values("id","name")),safe=False)


    def put(self, request):
        ret = {"status":0}
        data = QueryDict(request.body)
        uid = data.get("uid","")
        gid = data.get("gid","")

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

    def delete(self,request):
        ret = {"status":0}
