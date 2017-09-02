from django.conf.urls import include, url
from . import views, user, group

urlpatterns = [
    # 视图函数实现登录
        #url(r'^login/$', views.login_view, name='user_login'),
    # 模板视图实现登录
        url(r'^login/$', views.UserLoginView.as_view(), name='user_login'),
    # 视图函数实现退出
        #url(r'^logout/$', views.logout_view, name='user_logout'),
    # 类视图实现退出
        url(r'^logout/$', views.LogoutView.as_view(), name='user_logout'),
    # 视图函数
        #url(r'^user/list/$', views.user_list_view, name='user_list'),
    # 类视图
        #url(r'^user/list/$', views.UserListView.as_view(), name='user_list'),
    # ListView
        url(r'^user/list/$', user.UserListView.as_view(), name='user_list'),

        url(r'^user/', include([
            url(r'modify/', include([
                url(r'^status/$', user.ModifyUserStatusView.as_view(), name="user_modify_status"),
                url(r'^group/$', user.ModifyUserGroupView.as_view(), name="user_modify_group"),
            ]))
        ])),

        url(r'^group/', include([
            url(r'^$', group.GroupListView.as_view(), name='group_list'),
            url(r'^create/$', group.GroupCreateView.as_view(), name='group_create'),
            url(r'^userlist/$', group.GroupUserList.as_view(), name='group_userlist'),
        ])),
]
