from django.conf.urls import url, include
from resources import idc, views

urlpatterns = [
    url(r'^idc/', include([
        url(r'^list/$', idc.IdcListView.as_view(), name="idc_list"),
        url(r'^add/$', idc.IdcCreateView.as_view(), name="idc_add"),
    ])),

]
