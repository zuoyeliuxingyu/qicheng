from django.views.generic import ListView
from django.contrib.auth.models import User
#from accounts.views import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class UserListView(LoginRequiredMixin,ListView):
    template_name = 'user/userlist.html'
    model = User
    paginate_by = 8