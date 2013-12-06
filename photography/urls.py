from django.conf.urls import patterns, url
from django.conf import settings

from photography import views
from dhp.feeds import LatestPhotosFeed

urlpatterns = patterns('',
  url(r'^$', views.IndexView.as_view(), name='photography'),
  url(r'^album/(?P<album_id>[\w\-]+)/$', views.AlbumView.as_view(), name='album'),
  url(r'^photo/(?P<photo_id>[\w\-]+)/$', views.PhotographView.as_view(), name='photo'),
  url(r'^feed/$', LatestPhotosFeed()),
)
