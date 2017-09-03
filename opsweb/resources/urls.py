#!/usr/bin/python
# coding=utf8

from django.conf.urls import include, url
from . import views, idc


urlpatterns = [
    url(r'idc/', include([
        url(r'list/$', idc.IdcListView.as_view(), name='idc_list'),     # idc 展示页 url
        url(r'add/$', idc.AddIdcView.as_view(), name='idc_add'),     # idc 增加页 url
        url(r'delete/$', idc.DeleteIdcView.as_view(), name='idc_delete'),   # idc 删除 url
        url(r'get/$', idc.IdcMoreView.as_view(), name='idc_get'),   # idc ajax get url
    ]))

]
