from datetime import datetime

from django.views.generic import View
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.template import RequestContext, Template

from blog.models import Post


class PostView(View):
    def get(self, request, *args, **kwargs):
        matching_posts = Post.objects.filter(slug=kwargs.get('slug'))

        if not request.user.is_authenticated():
            right_now = datetime.now()
            matching_posts = matching_posts.filter(go_live_date__lte=right_now).exclude(take_down_date__lte=right_now)

        if len(matching_posts) != 1:
            raise Http404('No published post with slug \'{}\' was found'.format(kwargs.get('slug')))
        else:
            post = matching_posts[0]

        initial_template_string = render_to_string('blog/post.html', dictionary={'postbody': post.body}, context_instance=RequestContext(request))

        context = RequestContext(request)
        context['post'] = post
        return HttpResponse(Template(initial_template_string).render(context))