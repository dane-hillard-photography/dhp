from django.conf.urls import patterns, url

from photography import views
from dhp.feeds import LatestPhotosFeed

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='photography'),
    url(r'^album/(?P<album_id>[\w\-]+)/$', views.AlbumView.as_view(), name='album'),
    url(r'^photo/(?P<photo_id>[\w\-]+)/$', views.PhotographView.as_view(), name='photo'),
    url(r'^photoset/$', views.PhotoSetListView.as_view(), name='photoset_list'),
    url(r'^photoset/(?P<photoset_id>[\w\-]+)/(?P<photoset_slug>[\w\-]+)/$', views.PhotoSetView.as_view(), name='photoset'),
    url(r'^feed/$', LatestPhotosFeed(), name='feed'),
)
