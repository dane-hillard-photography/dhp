from django.conf.urls import patterns, url

from photography import views
from dhp.feeds import LatestPhotosFeed

urlpatterns = patterns(
    '',
    url(r'^$', views.PhotoSetListView.as_view(), name='photography'),
    url(r'^photo/(?P<photo_id>[\w\-]+)/$', views.PhotographView.as_view(), name='photo'),
    url(r'^photoset/(?P<photoset_id>[\w\-]+)/$', views.PhotoSetView.as_view(), name='photoset'),
    url(r'^photoset/(?P<photoset_id>[\w\-]+)/(?P<photoset_slug>[\w\-]+)/$', views.PhotoSetView.as_view(), name='photoset'),
    url(r'^feed/$', LatestPhotosFeed(), name='feed'),
)
