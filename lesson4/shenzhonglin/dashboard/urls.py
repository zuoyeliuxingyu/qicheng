
from django.conf.urls import url, include
from dashboard import views, statuss

urlpatterns = [
    # url(r'^$', views.index, name="index"),
    url(r'^$', views.IndexView.as_view(), name="index"),

    url(r'^success/(?P<next>[\s\S]*)/$', statuss.SuccessView.as_view(), name="success"),
    url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', statuss.ErrorView.as_view(), name="error"),

]