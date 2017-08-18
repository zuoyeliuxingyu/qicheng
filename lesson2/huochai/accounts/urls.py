from django.conf.urls import include, url
from . import views, user

urlpatterns = [
#        url(r'^login/$', views.login_view, name='user_login'),
        url(r'^login/$', views.Login_View.as_view(), name='user_login'),
#        url(r'^logout/$', views.logout_view, name='user_logout'),
        url(r'^logout/$', views.Logout_View.as_view(), name='user_logout'),
        url(r'^user/list/$', views.UserListView.as_view(), name='user_list')
#        url(r'^user/list/$', user.UserListView.as_view(), name='user_list'),
        ]
