from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'about/index.html'


class PricingView(TemplateView):
    template_name = 'about/pricing.html'
