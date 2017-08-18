from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^user/(?P<id>[0-9]{2})/(?P<name>[a-z]+)/(?P<age>[0-9]{1,2})/', views.user_details, name='id')
]
