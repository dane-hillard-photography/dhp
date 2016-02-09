from datetime import datetime

from django.views import generic

from blog.models import Post


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        right_now = datetime.now()
        context['latest_posts'] = Post.objects.filter(go_live_date__lte=right_now).exclude(take_down_date__lte=right_now).order_by('-go_live_date')[:5]

        return context
