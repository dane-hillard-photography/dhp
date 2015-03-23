from datetime import datetime

from django.views import generic
from django.db.models import Q

from blog.models import Post


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(Q(date_created__lte=datetime.now()) & Q(published=True))[:3]
        return context
