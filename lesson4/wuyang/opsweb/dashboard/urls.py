from django.conf.urls import include, url

from . import views
from . import mytest
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    # myself test
    url(r'^mysuccess/',mytest.SuccessView.as_view(),name='mysuccess'),



    url(r'^success/(?P<next>[\s\S]*)/$', views.SuccessView.as_view(), name='success'),
    url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', views.ErrorView.as_view(), name="error"),
]
# /error/jump_field/errmsg/
