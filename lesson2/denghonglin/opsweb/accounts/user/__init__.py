from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# 分页的页码之显示15个记录，显示当前页的前7个与后7个
class UserListView(LoginRequiredMixin,ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 8
    before_index = 7
    after_index = 6

    def get_context_data(self, **kwargs):
        context = super(UserListView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        return context

    def get_page_range(self,page_obj):
        start_index = page_obj.number - self.before_index
        if start_index < 0:
            start_index = 0
        return page_obj.paginator.page_range[start_index:page_obj.number + self.after_index]
