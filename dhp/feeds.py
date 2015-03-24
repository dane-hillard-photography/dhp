from datetime import datetime

from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed

from photography.models import Photograph
from blog.models import Post


class LatestPhotosFeed(Feed):
    title = "Dane Hillard Photography"
    link = "http://www.danehillard.com"
    description_template = "feeds/latest_photos_description.html"

    @staticmethod
    def items():
        return Photograph.objects.filter(public=True).order_by('-published_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('photography:photo', args=[item.uuid])


class LatestPostsFeed(Feed):
    title = 'Dane Hillard Photography'
    link = 'http://www.danehillard.com'
    description_template = 'feeds/latest_posts_description.html'

    @staticmethod
    def items():
        right_now = datetime.now()
        return Post.objects.filter(go_live_date__lte=right_now).exclude(take_down_date__lte=right_now).order_by('-date_created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.subtitle or 'Dane Hillard Photography'

    def item_link(self, item):
        return reverse('blog:post', args=[item.slug])