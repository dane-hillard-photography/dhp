import sys

from django.utils import timezone
from django.views import generic
from django.shortcuts import get_object_or_404

from photography.models import Photograph, Album

class IndexView(generic.ListView):
  template_name = 'photography/index.html'
  context_object_name = 'album_list'

  def get_queryset(self):
    return Album.objects.filter(
      published_date__lte=timezone.now(),
      public=True)

class PhotographView(generic.DetailView):
  template_name = 'photography/photograph.html'

  def get_object(self):
    return get_object_or_404(Photograph, uuid=self.kwargs['photo_id'])

class AlbumView(generic.DetailView):
  template_name = 'photography/album.html'

  def get_object(self):
    return get_object_or_404(Album, uuid=self.kwargs['album_id'])
