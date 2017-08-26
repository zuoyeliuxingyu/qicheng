from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^user/(?P<id>20)/(?P<age>[0-9]{2})/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-31]{2})/$', views.userdetail), #练习url函数传参，位置参数
]
