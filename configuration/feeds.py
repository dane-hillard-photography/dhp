from datetime import datetime

from django.contrib.syndication.views import Feed
from django.urls import reverse

from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'Dane Hillard Photography'
    link = 'https://www.danehillard.com'
    description_template = 'feeds/latest_posts_description.html'

    @staticmethod
    def items():
        right_now = datetime.now()
        return Post.objects.filter(go_live_date__lte=right_now).exclude(take_down_date__lte=right_now).order_by('-date_created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.subtitle or 'Dane Hillard Photography'

    def item_link(self, item):
        return reverse('blog:post', args=[item.slug])
