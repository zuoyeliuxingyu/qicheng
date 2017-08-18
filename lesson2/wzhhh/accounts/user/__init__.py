from django.views.generic import ListView
from django.contrib.auth.models import User
from accounts.views import LoginRequiredMixin
from django.core.paginator import Paginator

#Homework 3: Express limited pages
class UserListView(LoginRequiredMixin, ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 5
    scope = 7

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
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
        return context
