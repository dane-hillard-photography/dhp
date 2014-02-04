from django.conf.urls import patterns, url

from music import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='music'),
)
