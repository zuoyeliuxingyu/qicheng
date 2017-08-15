from django.conf.urls import include,url
from . import views,user

urlpatterns = [
    url(r'^login/$',views.LoginView.as_view(),name='user_login'),
    url(r'^logout/$',views.logout_view,name='user_logout'),
    url(r'^user/list/$',user.UserListView.as_view(),name='user_list'),
]
