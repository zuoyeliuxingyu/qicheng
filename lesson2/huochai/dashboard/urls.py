from django.conf.urls import include, url
from . import views


urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^user/(?P<id>[0-9]{4})/(?P<month>[0-9]{2})/$', views.userdetail,{'foo':'bar'}),
        ]
