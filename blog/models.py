from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse

from photography.models import Photograph


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    go_live_date = models.DateTimeField('Date and time to publish this post', blank=True, null=True, default=datetime.now)
    take_down_date = models.DateTimeField('Date and time to unpublish this post', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    feature_image = models.ForeignKey(Photograph, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})

    def published(self):
        right_now = datetime.now()
        if (self.go_live_date and self.go_live_date <= right_now) and (not self.take_down_date or right_now < self.take_down_date):
            return True
        return False
    published.boolean = True