import logging
from datetime import datetime

from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.template import RequestContext, Template

from blog.models import Post

LOGGER = logging.getLogger(__name__)


def post_view(request, slug):
    right_now = datetime.now()
    matching_posts = Post.objects.select_related('feature_image').prefetch_related('related_links').filter(slug=slug)

    if not any([request.user.is_authenticated, getattr(request, 'is_whitelisted_crawler', False)]):
        matching_posts = [
            post
            for post in matching_posts
            if not post.take_down_date
            or post.take_down_date <= right_now
        ]

        matching_posts = [
            post
            for post in matching_posts
            if not post.go_live_date
            or post.go_live_date <= right_now
        ]

    try:
        post = matching_posts[0]
    except IndexError:
        raise Http404('Post "{}" does not exist'.format(slug))

    context = RequestContext(request)

    initial_template_string = render_to_string(
        request=request,
        template_name='blog/post.html',
        context={'postbody': post.body}
    )

    context.update({
        'post': post,
        'previous_post': post.get_previous_post(),
        'next_post': post.get_next_post()
    })

    return HttpResponse(Template(initial_template_string).render(context))
