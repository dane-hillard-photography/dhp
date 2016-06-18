from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class BrandingView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'branding/branding.html'
