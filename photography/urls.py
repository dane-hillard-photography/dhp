from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from photography import views

urlpatterns = patterns('',
  url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^album/(?P<album_id>[\w\-]+)/$', views.AlbumView.as_view(), name='album'),
  url(r'^photo/(?P<photo_id>[\w\-]+)/$', views.PhotographView.as_view(), name='photo'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
