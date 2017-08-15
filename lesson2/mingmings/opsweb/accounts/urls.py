#!/usr/bin/python
# coding=utf8

from django.conf.urls import include, url
from . import views, user


urlpatterns = [

    url(r'^login/$', views.LoginView.as_view(), name='user_login'),     # 登录 url
    url(r'^logout/$', views. LogoutView.as_view(), name='user_logout'),     # 登出 url
    # url(r'^user/list/$', views.User_TemplateView.as_view(), name='user_list'),
    # url(r'^user/list/$', views.User_TemplateView.as_view()),
    url(r'^user/list/$', user.UserListView.as_view(), name='user_list'),        # 用户展示页

]