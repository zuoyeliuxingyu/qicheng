from django.conf.urls import include, url
from . import views, user, group,myuser

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='user_login'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name="user_logout"),
    #url(r'^user/list/$', views.UserListView.as_view(), name="user_list"),
    url(r'^user/list/$', user.UserListView.as_view(), name="user_list"),

    url(r'^user/myuserlist/$',myuser.UserListView.as_view(),name="my_user_list"),

    url(r'^user/', include([
        url(r'^modify/', include([
            url(r'^mystatus/$',myuser.ModifyUserStatusView.as_view(),name="myuser_modify_status"),
            url(r'^status/$', user.ModifyUserStatusView.as_view(), name="user_modify_status"),
            url(r'^group/$', user.ModifyUserGroupView.as_view(), name="user_modify_group"),
        ]))
    ])),

    url(r'^group/', include([
        url(r'^$', group.GroupListView.as_view(), name="group_list"),
        url(r'^create/$', group.GroupCreateView.as_view(), name="group_create"),
        url(r'^show_users/$', group.GroupUserListView.as_view(), name="group_user_list"),
        url(r'^delete_user/$',group.DelGroupUserView.as_view(),name="del_group_user")
    ])),
]
