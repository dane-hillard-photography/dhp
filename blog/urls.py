from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[\w\-]+)/$', views.PostView.as_view(), name='post'),
)
