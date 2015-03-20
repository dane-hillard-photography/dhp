from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from blog import views

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[\w\-]+)/$', views.PostView.as_view(), name='post'),
    url(r'^tools/writer/$', login_required(views.WriterView.as_view()), name='writer'),
)
