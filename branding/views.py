from django.shortcuts import render
from django.views.generic import TemplateView


class BrandingView(TemplateView):
    template_name = 'branding/branding.html'
