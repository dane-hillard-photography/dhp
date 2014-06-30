from django.views import generic
from django.db.models import Q
from django.utils import timezone

from photography.models import PhotoSet

class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['latest_photosets'] = PhotoSet.objects.filter(
            Q(published_date__lte=timezone.now()))[:3]
        return context
