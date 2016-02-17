from datetime import datetime

from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.template import RequestContext, Template
from django.views.decorators.http import last_modified
from django.views.decorators.cache import cache_control
from django.shortcuts import get_list_or_404

from blog.models import Post


def post_last_modified(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        return post.date_modified
    except Post.DoesNotExist:
        return None


@cache_control(max_age=3600 * 24)
@last_modified(post_last_modified)
def post_view(request, slug):
    right_now = datetime.now()
    matching_posts = Post.objects.filter(slug=slug)

    if not any([request.user.is_authenticated(), getattr(request, 'is_whitelisted_crawler', False)]):
        matching_posts = matching_posts.exclude(take_down_date__lte=right_now)
        matching_posts = get_list_or_404(matching_posts, go_live_date__lte=right_now)

    try:
        post = matching_posts[0]
    except IndexError:
        raise Http404

    context = RequestContext(request)
    initial_template_string = render_to_string(request=request, template_name='blog/post.html', context={'postbody': post.body})
    context.update({'post': post, 'previous_post': post.get_previous_post(), 'next_post': post.get_next_post()})

    return HttpResponse(Template(initial_template_string).render(context))
