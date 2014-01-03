from django.views import generic
from django.db.models import Q
from django.utils import timezone

from photography.models import Photograph

class IndexView(generic.TemplateView):
  template_name = 'home/index.html'

  def get_context_data(self, **kwargs):
	  context = super(IndexView, self).get_context_data(**kwargs)
	  context['latest_photos'] = Photograph.objects.filter(
			  Q(published_date__lte=timezone.now()) & (Q(public=True) | Q(user_id=self.request.user.id))).order_by('-published_date')[:5]
	  return context
