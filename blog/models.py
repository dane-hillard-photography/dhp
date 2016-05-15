from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse

from photography.models import Photograph


class Link(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title


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
    meta_description = models.CharField(max_length=150, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    go_live_date = models.DateTimeField('Date and time to publish this post', blank=True, null=True)
    take_down_date = models.DateTimeField('Date and time to unpublish this post', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    feature_image = models.ForeignKey(Photograph, blank=True, null=True, related_name='featured_in')
    related_links = models.ManyToManyField(Link, blank=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_now():
        return datetime.now()

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})

    def published(self):
        right_now = self.get_now()
        print(right_now)
        print(self.go_live_date)
        if (self.go_live_date and self.go_live_date <= right_now) and (not self.take_down_date or right_now < self.take_down_date):
            return True
        return False
    published.boolean = True

    @classmethod
    def get_live_posts(cls):
        right_now = cls.get_now()
        return Post.objects.filter(go_live_date__lte=right_now).exclude(take_down_date__lte=right_now)

    def get_previous_posts(self):
        all_live_posts = self.get_live_posts()
        cutoff_date = self.go_live_date or self.get_now()
        return all_live_posts.filter(go_live_date__lt=cutoff_date).order_by('-go_live_date')

    def get_following_posts(self):
        all_live_posts = self.get_live_posts()
        cutoff_date = self.go_live_date or self.get_now()
        return all_live_posts.filter(go_live_date__gt=cutoff_date).order_by('go_live_date')

    def get_previous_post(self):
        previous_posts = self.get_previous_posts()
        return previous_posts[0] if previous_posts else None

    def get_next_post(self):
        following_posts = self.get_following_posts()
        return following_posts[0] if following_posts else None
