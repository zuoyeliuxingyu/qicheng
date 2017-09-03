#!/usr/bin/python
# coding=utf8

from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^user/(?P<id>20)/$', views.url_test),     # url 的位置参数和关键字参数
    url(r'^success/(?P<next>[\s\S]*)/$', views.SuccessView.as_view(), name='success'),
    url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', views.ErrorView.as_view(), name="error"),   #

]