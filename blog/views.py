from django.views.generic import View
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.template.loader import get_template_from_string, render_to_string

from blog.models import Post


class PostView(View):
    def get(self, request, *args, **kwargs):
        matching_posts = Post.objects.filter(slug=kwargs.get('slug')).filter(published=True)
        if len(matching_posts) != 1:
            raise Http404('No published post with slug \'{}\' was found'.format(kwargs.get('slug')))
        else:
            post = matching_posts[0]

        template_string = '{% extends \'__base.html\' %}{% load snippets %}{% block content %}' + post.body + '{% endblock %}'
        template = get_template_from_string(template_string)
        return HttpResponse(template.render(RequestContext(request)))


class WriterView(View):
    def get(self, request, *args, **kwargs):
        template_string = render_to_string('blog/post_writer.html')
        template = get_template_from_string(template_string)
        return HttpResponse(template.render(RequestContext(request)))