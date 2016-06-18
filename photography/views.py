from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from photography.models import Photograph


class PortfolioView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'photography/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['photos'] = Photograph.objects.filter(in_portfolio=True)
        return context
