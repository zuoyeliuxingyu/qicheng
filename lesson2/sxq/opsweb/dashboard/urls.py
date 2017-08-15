from django.conf.urls import url
from . import views

urlpatterns = [
#    url(r'^$', views.index, name='index'),

     url('^$', views.IndexView.as_view(), name="index"),

# 位置参数
#    url(r'^user/([0-9]{4})/([0-9]{2})/([0-9]{2})/$', views.user_detail, name='user'),
# 关键字参数
#     url(r'^user/(?P<id>20)/(?P<year>[0-9]{4})/$', views.user_detail, name="user"),
#     url(r'^user/(?P<id>20)/$', views.user_detail, name="user"),
]
