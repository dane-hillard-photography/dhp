from datetime import datetime

from django.views.generic import YearArchiveView, MonthArchiveView
from django.http import HttpResponse
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
    matching_posts = Post.objects.filter(slug=slug)

    if not request.user.is_authenticated():
        right_now = datetime.now()
        matching_posts = matching_posts.exclude(take_down_date__lte=right_now)
        matching_posts = get_list_or_404(matching_posts, go_live_date__lte=right_now)

    post = matching_posts[0]

    context = RequestContext(request)
    initial_template_string = render_to_string('blog/post.html', dictionary={'postbody': post.body}, context_instance=context)
    context.update({'post': post})

    return HttpResponse(Template(initial_template_string).render(context))


class PostYearArchiveView(YearArchiveView):
    model = Post
    date_field = 'go_live_date'
    queryset = Post.objects.exclude(take_down_date__lte=datetime.now())


class PostMonthArchiveView(MonthArchiveView):
    model = Post
    date_field = 'go_live_date'
    month_format = '%m'
    queryset = Post.objects.exclude(take_down_date__lte=datetime.now())
