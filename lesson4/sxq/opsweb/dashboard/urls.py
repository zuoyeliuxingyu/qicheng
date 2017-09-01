from django.conf.urls import url
#from django.contrib import admin
from . import views

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
#    url(r'^$', views.index, name='index'),
     url('^$', views.IndexView.as_view(), name="index"),
     url('^success/(?P<next>[\s\S]*)/$', views.SuccessView.as_view(), name="success"),
     url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', views.ErrorView.as_view(), name="error"),

# 位置参数
#    url(r'^user/([0-9]{4})/([0-9]{2})/([0-9]{2})/$', views.user_detail, name='user'),
# 关键字参数
#    url(r'^user/(?P<id>20)/(?P<year>[0-9]{4})/$', views.user_detail, name="user"),
#    url(r'^user/(?P<id>20)/$', views.user_detail, name="user"),
]
