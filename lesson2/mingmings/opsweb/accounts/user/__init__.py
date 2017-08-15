# coding=utf-8
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.models import User


class UserListView(ListView):

    template_name = "user/userlist.html"
    model = User
    paginate_by = 10        # 每页展示多少对象
    before_index = 7        # 当前页往前几页
    after_index = 7         # 当前页往后几页

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
        return context

    def get_page_range(self, page_obj):
        """
        分页处理逻辑
            page_obj 是需要传递的参数，为当前页的模型对象，可以通过遍历的方式得到该对象里的内容

        处理思路：
            - 能够让用户循环的全部 user 的 list，称之为外部 list
            -  最终展示的页码的集合一定是这个外部 list 内的一个更小的 list，是上述外部 list 的子集
        """

        # 开始序列号 = 当前页码号 - 后置序列号
        start_index = page_obj.number - self.before_index

        # 应对开始序列异常的情况，最小不能为 0
        if start_index < 0:
            start_index = 0

        # 最终在页面上供展示的循环的 list
        page_range = page_obj.paginator.page_range[start_index: page_obj.number + self.after_index]
        return page_range