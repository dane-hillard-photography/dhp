from django.db.models import Q
from django.views import generic
from django.shortcuts import get_object_or_404

from photography.models import Photograph, PhotoSet
from dhp import settings


class PhotographView(generic.DetailView):
    template_name = 'photography/photograph.html'

    def get_object(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return get_object_or_404(Photograph, uuid=self.kwargs['photo_id'])
        else:
            return get_object_or_404(
                Photograph, Q(uuid=self.kwargs['photo_id']) & (Q(public=True) | Q(user_id=self.request.user.id))
            )

    def get_context_data(self, **kwargs):
        context = super(PhotographView, self).get_context_data(**kwargs)
        context['photosets'] = self.get_object().photosets_in.all()
        return context


class PhotoSetView(generic.DetailView):
    template_name = 'photography/photoset.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(PhotoSet, id=self.kwargs['photoset_id'])

    def get_context_data(self, **kwargs):
        context = super(PhotoSetView, self).get_context_data(**kwargs)
        return context


class PhotoSetListView(generic.ListView):
    template_name = 'photography/photoset_list.html'
    context_object_name = 'photoset_list'

    def get_queryset(self):
        return PhotoSet.objects.all()