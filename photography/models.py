import os
import uuid
from PIL import Image as PImage
from PIL import ImageOps as PImageOps
from PIL import ExifTags as PExif
from tempfile import *

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db.models import F
from django.db.models import Max

from dhp.settings import MEDIA_ROOT, MEDIA_URL

def generate_uuid():
  return str(uuid.uuid4())

def max_sort_order():
  return Album.objects.all().aggregate(Max('sort_order'))['sort_order__max'] + 1

def get_file_path(instance, filename):
  ext = filename.split('.')[-1]
  saveFilename = "%s.%s" % (instance.uuid, ext)
  return os.path.join(instance.directory, saveFilename)

class Album(models.Model):
  class Meta:
    ordering = ['sort_order',]

  published_date = models.DateTimeField()
  title = models.CharField(max_length=255)
  public = models.BooleanField(default=True)
  uuid = models.CharField("UUID", max_length=36, unique=True, default=generate_uuid, editable=False)
  sort_order = models.IntegerField(blank=True, null=True, default=max_sort_order)
  user = models.ForeignKey(User, blank=True, null=True)

  def __unicode__(self):
    return self.title

  def photos(self):
    photoList = ['<a href="%s">%s</a>' % (reverse('admin:photography_photograph_change', args=(photo.id,)), photo.title) for photo in self.photograph_set.all().reverse()]
    return ", ".join(photoList)
  photos.allow_tags = True

  def get_absolute_url(self):
    return reverse('photography:album', kwargs={'album_id': self.uuid})

  def save(self, *args, **kwargs):
    if (self.pk is not None):
      current = Album.objects.get(pk=self.pk)
      currentOrder = current.sort_order
      newOrder = self.sort_order

      if (currentOrder != newOrder):
        existingAlbum = Album.objects.filter(sort_order=newOrder)

        if existingAlbum:
          Album.objects.filter(pk=self.pk).update(sort_order=None)

          if (currentOrder < newOrder):
            albums = Album.objects.filter(sort_order__gt=currentOrder, sort_order__lte=newOrder)
            for album in albums:
              album.sort_order -= 1
              super(Album, album).save()
          elif (currentOrder > newOrder):
            albums = Album.objects.filter(sort_order__lt=currentOrder, sort_order__gte=newOrder).reverse()
            for album in albums:
              album.sort_order += 1
              super(Album, album).save()

    super(Album, self).save(*args, **kwargs)

class Tag(models.Model):
  class Meta:
    ordering = ['tag',]

  tag = models.CharField(max_length=255, unique=True)

  def __unicode__(self):
    return self.tag

class Photograph(models.Model):
  class Meta:
    ordering = ['-published_date',]

  ORIENTATION_CHOICES = (
    ('P', 'Portrait'),
    ('L', 'Landscape'),
    ('S', 'Square'),
  )
  
  directory = "images/uncropped"

  published_date = models.DateTimeField()
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  image = models.ImageField(upload_to=get_file_path)
  width = models.IntegerField(blank=True, null=True)
  height = models.IntegerField(blank=True, null=True)
  public = models.BooleanField(default=True)
  albums = models.ManyToManyField(Album)
  tags = models.ManyToManyField(Tag)
  orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES, editable=False)
  uuid = models.CharField("UUID", max_length=36, unique=True, default=generate_uuid, editable=False)

  user = models.ForeignKey(User, blank=True, null=True)

  thumbnail_large = models.ImageField(upload_to="images/large", blank=True, null=True)
  thumbnail_medium = models.ImageField(upload_to="images/medium", blank=True, null=True)
  thumbnail_small = models.ImageField(upload_to="images/small", blank=True, null=True)
  thumbnail_square = models.ImageField(upload_to="images/square", blank=True, null=True)

  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    return reverse('photography:photo', kwargs={'photo_id': self.uuid})

  def save(self, *args, **kwargs):
    super(Photograph, self).save(*args, **kwargs)
    im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
    self.width, self.height = im.size
    ratioDivisor = self.height
    thumbnailSize = (200, 200)

    if self.width > self.height:
      self.orientation = "L"
      ratioDivisor = self.width
    elif self.width < self.height:
      self.orientation = "P"
    else:
      self.orientation = "S"
      
    ratio = 800.0 / ratioDivisor
    im.thumbnail((self.width * ratio, self.height * ratio), PImage.ANTIALIAS)
    tf = NamedTemporaryFile()
    im.save(tf.name, im.format)
    self.thumbnail_large.save(self.image.name, File(open(tf.name)), save=False)
    tf.close()

    ratio = 500.0 / ratioDivisor
    im.thumbnail((self.width * ratio, self.height * ratio), PImage.ANTIALIAS)
    tf = NamedTemporaryFile()
    im.save(tf.name, im.format)
    self.thumbnail_medium.save(self.image.name, File(open(tf.name)), save=False)
    tf.close()

    ratio = 200.0 / ratioDivisor
    im.thumbnail((self.width * ratio, self.height * ratio), PImage.ANTIALIAS)
    tf = NamedTemporaryFile()
    im.save(tf.name, im.format)
    self.thumbnail_small.save(self.image.name, File(open(tf.name)), save=False)
    tf.close()

    thumbSquare = PImageOps.fit(im, thumbnailSize, PImage.ANTIALIAS)
    fn, ext = os.path.splitext(self.image.name)
    tf = NamedTemporaryFile()
    thumbSquare.save(tf.name, im.format)
    self.thumbnail_square.save(self.image.name, File(open(tf.name)), save=False)
    tf.close()

    super(Photograph, self).save(*args, **kwargs)

  def size(self):
    return "%s x %s" % (self.width, self.height)

  def admin_thumbnail(self):
    if self.image:
      return '<img src="%s" width="60" />' % self.thumbnail_small.url
    else:
      return 'No image available'
  admin_thumbnail.short_description = 'Thumbnail'
  admin_thumbnail.allow_tags = True

  def __unicode__(self):
    return self.title

class Service(models.Model):
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=1000)
  price = models.DecimalField(max_digits=6, decimal_places=2, null=True) 

  def __unicode__(self):
    return self.title
