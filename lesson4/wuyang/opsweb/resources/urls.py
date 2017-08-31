from django.conf.urls import include, url

from . import idc,views

urlpatterns = [
    url(r'idc/', include([
        url(r'add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'list/$', idc.ListIdcView.as_view(), name="idc_list"),
        url(r'delete/$', idc.DeleteIdcView.as_view(), name="idc_delete"),
    ]))
]
