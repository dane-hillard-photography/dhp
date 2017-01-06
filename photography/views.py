from django.views.generic import TemplateView

from photography.models import Photograph


class PortfolioView(TemplateView):
    template_name = 'photography/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['photos'] = Photograph.objects.filter(in_portfolio=True).order_by('-pk')
        return context

def do_nothing(request):
    return ('foo'+ 'bar')
