from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^user/(?P<id>[0-9]{2})/(?P<name>[a-z]+)/(?P<age>[0-9]{1,2})/', views.user_details, name='id'),
    url(r'^success/(?P<next>[\s\S]*)/$', views.SuccessView.as_view(), name='success'),
    url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', views.ErrorView.as_view(), name="error"),
]
# /error/jump_field/errmsg/