from datetime import datetime

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from blog.models import Post


class SiteSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    @staticmethod
    def lastmod(obj):
        return timezone.now()

    def location(self, obj):
        return reverse(obj)


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        right_now = datetime.now()
        return Post.objects.filter(go_live_date__lte=right_now).exclude(take_down_date__lte=right_now)

    @staticmethod
    def lastmod(obj):
        return obj.date_modified

    def location(self, obj):
        return reverse('blog:post', kwargs={'slug': obj.slug})
