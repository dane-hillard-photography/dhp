from django.views import generic

from blog.models import Post


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['posts'] = Post.get_live_posts().select_related('feature_image').order_by('-go_live_date')

        return context
