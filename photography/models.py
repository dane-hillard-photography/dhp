import os
import uuid
import datetime
from tempfile import *

from PIL import Image as PImage
from PIL import ImageOps as PImageOps

from django.db import models
from django.db.models import Max
from django.core.files import File
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from dhp.settings import MEDIA_ROOT

def generate_uuid():
    return str(uuid.uuid4())

def max_sort_order():
    current_max = Album.objects.all().aggregate(Max('sort_order'))['sort_order__max']
    if current_max is None:
        current_max = 0
    return current_max + 1

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    save_filename = '{uuid}.{ext}'.format(uuid=instance.uuid, ext=ext)
    return os.path.join(instance.directory, save_filename)

class Album(models.Model):
    class Meta:
        ordering = ['sort_order']

    title = models.CharField(max_length=255)
    uuid = models.CharField('UUID', max_length=36, unique=True, default=generate_uuid, editable=False)
    public = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=datetime.datetime.now)
    sort_order = models.IntegerField(blank=True, null=True, default=max_sort_order)
    user = models.ForeignKey(User, blank=True, null=True, default=User.objects.get(username='dane').id)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photography:album', kwargs={'album_id': self.uuid})

class Photograph(models.Model):
    class Meta:
        ordering = ['-published_date']

    ORIENTATION_CHOICES = (
        ('P', 'Portrait'),
        ('L', 'Landscape'),
        ('S', 'Square'),
    )
  
    directory = os.path.join('images', 'uncropped')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL)
    public = models.BooleanField(default=True)
    orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES, editable=False)
    uuid = models.CharField('UUID', max_length=36, unique=True, default=generate_uuid, editable=False)
    published_date = models.DateTimeField(default=datetime.datetime.now)

    user = models.ForeignKey(User, blank=True, null=True, default=User.objects.get(username='dane').id)

    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    l_height = models.IntegerField(blank=True, null=True)
    l_width = models.IntegerField(blank=True, null=True)
    m_height = models.IntegerField(blank=True, null=True)
    m_width = models.IntegerField(blank=True, null=True)
    sm_height = models.IntegerField(blank=True, null=True)
    sm_width = models.IntegerField(blank=True, null=True)
    sq_height = models.IntegerField(blank=True, null=True)
    sq_width = models.IntegerField(blank=True, null=True)

    image = models.ImageField(upload_to=get_file_path, height_field='height', width_field='width')
    
    thumbnail_large = models.ImageField(
        upload_to='images/large', blank=True, null=True, height_field='l_height', width_field='l_width')
    thumbnail_medium = models.ImageField(
        upload_to='images/medium', blank=True, null=True, height_field='m_height', width_field='m_width')
    thumbnail_small = models.ImageField(
        upload_to='images/small', blank=True, null=True, height_field='sm_height', width_field='sm_width')
    thumbnail_square = models.ImageField(
        upload_to='images/square', blank=True, null=True, height_field='sq_height', width_field='sq_width')

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('photography:photo', kwargs={'photo_id': self.uuid})
    
    def create_thumbnail(self, original_image, new_image, max_size):
        width, height = original_image.size
        ratio_divisor = height if height > width else width
        ratio = float(max_size) / ratio_divisor

        if width > height:
            self.orientation = "L"
        elif width < height:
            self.orientation = "P"
        else:
            self.orientation = "S"

        original_image.thumbnail((int(width * ratio), int(height * ratio)), PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        original_image.save(tf.name, original_image.format, quality=100)
        new_image.save(self.image.name, File(open(tf.name)), save=False)
        tf.close()

    def save(self, *args, **kwargs):
        super(Photograph, self).save(*args, **kwargs)
        image = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        
        thumbnail_size = (250, 250)
        thumb_square = PImageOps.fit(image, thumbnail_size, PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        thumb_square.save(tf.name, image.format, quality=100)
        self.thumbnail_square.save(self.image.name, File(open(tf.name)), save=False)
        tf.close()
      
        self.create_thumbnail(image, self.thumbnail_large, 800)
        self.create_thumbnail(image, self.thumbnail_medium, 500)
        self.create_thumbnail(image, self.thumbnail_small, 200)

        super(Photograph, self).save(*args, **kwargs)

    def size(self):
        return '{width} x {height}'.format(width=self.width, height=self.height)

    def admin_thumbnail(self):
        if self.image:
            return '<img src="{url}" width="60" />'.format(url=self.thumbnail_small.url)
        else:
            return 'No image available'
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def __unicode__(self):
        return self.title

class PhotoSet(models.Model):
    class Meta:
        ordering = ['-published_date']

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40)
    body = models.TextField()
    feature_photo = models.ForeignKey(Photograph, related_name='photosets_featured_in')
    photos = models.ManyToManyField(Photograph, related_name='photosets_in', )
    published_date = models.DateTimeField(default=datetime.datetime.now)

    def feature_photo_thumbnail(self):
        return '<img src="{url}" width="60" />'.format(url=self.feature_photo.thumbnail_small.url)
    feature_photo_thumbnail.short_description = 'Feature Photo'
    feature_photo_thumbnail.allow_tags = True