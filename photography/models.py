import os
import uuid
from PIL import Image as PImage
from PIL import ExifTags as PExif
from tempfile import *

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File

from dhp.settings import MEDIA_ROOT, MEDIA_URL

def generate_uuid():
  return str(uuid.uuid4())

def get_file_path(instance, filename):
  ext = filename.split('.')[-1]
  filename = "%s.%s" % (instance.uniq, ext)
  return os.path.join(instance.directory, filename)

class Album(models.Model):
  published_date = models.DateTimeField()
  title = models.CharField(max_length=255)
  public = models.BooleanField(default=True)
  uuid = models.CharField("UUID", max_length=36, unique=True, default=generate_uuid, editable=False)

  def __unicode__(self):
    return self.title

  def photos(self):
    photoList = ['<a href="%s">%s</a>' % (photo.image.url, photo.title) for photo in self.photograph_set.all()]
    return ", ".join(photoList)
  photos.allow_tags = True

class Tag(models.Model):
  tag = models.CharField(max_length=255)

  def __unicode__(self):
    return self.tag

class Photograph(models.Model):
  uniq = generate_uuid()
  directory = "images/uncropped"

  published_date = models.DateTimeField()
  title = models.CharField(max_length=255)
  image = models.ImageField(upload_to=get_file_path)
  width = models.IntegerField(blank=True, null=True)
  height = models.IntegerField(blank=True, null=True)
  public = models.BooleanField(default=True)
  albums = models.ManyToManyField(Album)
  tags = models.ManyToManyField(Tag)
  uuid = models.CharField("UUID", max_length=36, unique=True, default=uniq, editable=False)

  user = models.ForeignKey(User, blank=True, null=True)

  thumbnail_large = models.ImageField(upload_to="images", blank=True, null=True)
  thumbnail_medium = models.ImageField(upload_to="images", blank=True, null=True)
  thumbnail_small = models.ImageField(upload_to="images", blank=True, null=True)

  def save(self, *args, **kwargs):
    super(Photograph, self).save(*args, **kwargs)
    im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
    self.width, self.height = im.size

    ratio = 800.0 / self.width
    fn, ext = os.path.splitext(self.image.name)
    im.thumbnail((self.width * ratio, self.height * ratio), PImage.ANTIALIAS)
    thumb_fn = fn + "-large" + ext
    tf = NamedTemporaryFile()
    im.save(tf.name, im.format)
    self.thumbnail_large.save(thumb_fn, File(open(tf.name)), save=False)
    tf.close()

    ratio = 500.0 / self.width
    im.thumbnail((self.width * ratio, self.height * ratio), PImage.ANTIALIAS)
    thumb_fn = fn + "-medium" + ext
    tf = NamedTemporaryFile()
    im.save(tf.name, im.format)
    self.thumbnail_medium.save(thumb_fn, File(open(tf.name)), save=False)
    tf.close()

    ratio = 200.0 / self.width
    im.thumbnail((self.width * ratio, self.height * ratio), PImage.ANTIALIAS)
    thumb_fn = fn + "-small" + ext
    tf = NamedTemporaryFile()
    im.save(tf.name, im.format)
    self.thumbnail_small.save(thumb_fn, File(open(tf.name)), save=False)
    tf.close()

    super(Photograph, self).save(*args, **kwargs)

  def size(self):
    return "%s x %s" % (self.width, self.height)

  def admin_thumbnail(self):
    if self.image:
      return '<a href=' + self.image.url + '><img src="%s" width="60" /></a>' % self.thumbnail_small.url
    else:
      return 'No image available'
  admin_thumbnail.short_description = 'Thumbnail'
  admin_thumbnail.allow_tags = True

  def __unicode__(self):
    return self.title
