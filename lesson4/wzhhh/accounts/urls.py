from django.conf.urls import url, include
from . import views, user, group

urlpatterns = [
    #url(r'^login/$', views.login_view, name='user_login'),
    #url(r'^login/$', views.LoginView.as_view(), name='user_login'),
    url(r'^login/$', views.UserLoginView.as_view(), name='user_login'),
    #url(r'^logout/$', views.logout_view, name='user_logout'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='user_logout'),
    #url(r'^logout/$', views.LogoutTemplateView.as_view(), name='user_logout'),
    #url(r'^user/list/$', views.UserListView.as_view(), name='user_list'),
    url(r'^user/list/$', user.UserListView.as_view(), name='user_list'),

    url(r'^user/', include([
        url(r'^modify/', include([
            url(r'^status/$', user.ModifyUserStatusView.as_view(), name="user_modify_status"),
            url(r'^group/', user.ModifyUserGroupView.as_view(), name="user_modify_group"),
        ]))
    ])),

    url(r'^group/', include([
        url(r'^$', group.GroupListView.as_view(), name="group_list"),
        url(r'^userlist/', group.GroupUserListView.as_view(), name="group_user_list"),
        url(r'^create/$', group.GroupCreateView.as_view(), name="group_create"),
    ]))
]
