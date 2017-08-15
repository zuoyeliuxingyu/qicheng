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
        context['page_range'] = self.get_page_range(context['page_obj'])
        context['users'] = User.objects.all()
        context.update(self.request.GET.dict())
        # print(self.request.GET.dict())
        return context

    def get_page_range(self, page_obj):
        """分页处理逻辑"""

        # 开始序列号 = 当前页码号 - 后置序列号
        start_index = page_obj.number - self.before_index
        # 应对开始序列异常的情况，最小不能为 0
        if start_index < 0:
            start_index = 0

        # 最终在页面上供展示的循环的 list
        page_range = page_obj.paginator.page_range[start_index: page_obj.number + self.after_index]
        return page_range
