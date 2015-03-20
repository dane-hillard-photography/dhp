from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.template.loader import get_template_from_string, render_to_string

from blog.models import Post


class PostView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get('slug'))
        template_string = '{% extends \'__base.html\' %}{% load snippets %}{% block content %}' + post.body + '{% endblock %}'
        template = get_template_from_string(template_string)
        return HttpResponse(template.render(RequestContext(request)))


class WriterView(View):
    def get(self, request, *args, **kwargs):
        template_string = render_to_string('blog/post_writer.html')
        template = get_template_from_string(template_string)
        return HttpResponse(template.render(RequestContext(request)))