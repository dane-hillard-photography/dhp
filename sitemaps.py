from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from photography.models import Photograph, PhotoSet


class PhotographSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Photograph.objects.filter(published_date__lte=timezone.now(), public=True)

    @staticmethod
    def lastmod(obj):
        return obj.published_date

    @staticmethod
    def location(obj):
        return reverse('photography:photo', kwargs={'photo_id': obj.uuid})


class PhotoSetSitemap(Sitemap):
    changefreq = 'monthly'
    priority = .75

    def items(self):
        return PhotoSet.objects.all()

    @staticmethod
    def lastmod(obj):
        return obj.published_date

    @staticmethod
    def location(obj):
        return reverse('photography:photoset', kwargs={'photoset_id': obj.id, 'photoset_slug': obj.slug})


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
