from django.conf.urls import include, url
from . import views
urlpatterns = [
#        url(r'^$', views.index, name='index'),
        url(r'^$', views.IndexView.as_view(), name='index'),
#        url(r'^user/20/(?P<id>[0-9]{2})/$', views.userdetail),
        ]
