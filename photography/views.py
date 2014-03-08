from django.db.models import Q
from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404

from photography.models import Photograph, Album
from dhp import settings

class IndexView(generic.ListView):
    template_name = 'photography/index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Album.objects.all()
        else:
            return Album.objects.filter(
                Q(published_date__lte=timezone.now()) & (Q(public=True) | Q(user_id=self.request.user.id))
            ).order_by('sort_order')

class PhotographView(generic.DetailView):
    template_name = 'photography/photograph.html'

    def get_object(self):
        if self.request.user.is_superuser:
            return get_object_or_404(Photograph, uuid=self.kwargs['photo_id'])
        else:
            return get_object_or_404(
                Photograph, Q(uuid=self.kwargs['photo_id']) & (Q(public=True) | Q(user_id=self.request.user.id))
            )

    def get_context_data(self, **kwargs):
        context = super(PhotographView, self).get_context_data(**kwargs)
        context['social_media'] = settings.SOCIAL_MEDIA_HANDLES
        return context

class AlbumView(generic.DetailView):
    template_name = 'photography/album.html'

    def get_object(self):
        if self.request.user.is_superuser:
            return get_object_or_404(Album, uuid=self.kwargs['album_id'])
        else:
            return get_object_or_404(
                Album, Q(uuid=self.kwargs['album_id']) & (Q(public=True) | Q(user_id=self.request.user.id))
            )

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['social_media'] = settings.SOCIAL_MEDIA_HANDLES
        return context
