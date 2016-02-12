from django.views import generic

from blog.models import Post


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        all_live_posts = Post.get_live_posts().order_by('-go_live_date')

        dates = [post.go_live_date for post in all_live_posts]
        years = set([date.year for date in dates])
        context['posts'] = all_live_posts
        context['posts_by_year'] = {year: [post for post in all_live_posts if post.go_live_date.year == year] for year in years}

        return context
