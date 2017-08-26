
from django.conf.urls import url, include
from accounts import views, user, group

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name="user_login"),
    url(r'^logout/$', views.UserLogoutView.as_view(), name="user_logout"),

    url(r'^user/',include([
        url(r'^list/$', user.UserListView.as_view(), name="user_list"),
        url(r'^modify/', include([
            url(r'^status/$', user.ModifyUserStatusView.as_view(), name="user_modify_status"),
            url(r'group/$', user.ModifyUserGroupView.as_view(), name="user_modify_group"),
        ]))
    ])),

    url(r'^group/', include([
        url(r'^$', group.GroupListView.as_view(), name="group_list"),
        url(r'^create/$', group.GroupCreateView.as_view(), name="group_create"),
        url(r'^memberlist/(?P<gid>\d+)/$', group.GroupUserView.as_view(), name="group_memberlist"),
        # url(r'^memberlist/$', group.GroupUserView.as_view(), name="group_memberlist"),
    ]))
]