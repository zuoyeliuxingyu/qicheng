
from django.conf.urls import url, include
from accounts import views
from accounts import user, group

urlpatterns = [
    # url(r'login/$', views.login_view, name="user_login"),
    url(r'^login/$', views.UserLoginView.as_view(), name="user_login"),
    # url(r'logout/$', views.logout_view, name="user_logout"),
    url(r'^logout/$', views.UserLogoutView.as_view(), name="user_logout"),

    url(r'^user', include([
        # url(r'list/$', views.UserListView.as_view(), name="user_list"),
        url(r'^list/$', user.UserListView.as_view(), name="user_list"),
        url(r'^modify/', include([
            url(r'^status/$', user.ModifyUserStatusView.as_view(), name="modify_user_status"),
            url(r'^group/$', user.ModifyUserGroupView.as_view(), name="modify_user_group"),
        ]))
    ])),

    url(r'^group/',include([
        url(r'^$', group.GroupListView.as_view(), name="group_list"),
        url(r'^create/$', group.CreateGroupView.as_view(), name="create_group"),
        # url(r'groupuserlist/(?P<gid>\d+)$', group.GroupUserListView.as_view(), name="group_userlist"),
        url(r'^groupuserlist/$', group.GroupUserListView.as_view(), name="group_userlist"),
    ]))

]
