from django.views.generic import ListView,TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin



class UserListView(ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 10         #每页展示多少个数据
    before_index = 5         #当前页往前多少页
    after_index = 5          #当前页往后多少页


    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)   #基础父类属性

        #在给前端进行传递的变量
        context['page_range'] = self.get_page_range(context['page_obj']) #可以循环的page对象
        context['users'] = User.objects.all()    #所有 user对象

        #
        context.update(self.request.GET.dict())
        return context

    def get_page_range(self, page_obj):

        start_index = page_obj.number - self.before_index

        if start_index < 0:
            start_index = 0

        page_range = page_obj.paginator.page_range[start_index: page_obj.number + self.after_index]
        return page_range