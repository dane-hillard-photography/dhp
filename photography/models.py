import os
import uuid
import datetime
from tempfile import *

from PIL import Image as PImage
from PIL import ImageOps as PImageOps

from django.db import models
from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_delete


def generate_uuid():
    return str(uuid.uuid4())


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    save_filename = '{uuid}.{ext}'.format(uuid=instance.uuid, ext=ext)
    return os.path.join(settings.IMAGE_UPLOAD_PATH, save_filename)


class Photograph(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    uuid = models.CharField('UUID', max_length=36, unique=True, default=generate_uuid, editable=False)

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

        original_image.thumbnail((int(width * ratio), int(height * ratio)), PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        original_image.save(tf.name, original_image.format, quality=100)
        new_image.save(self.image.name, File(open(tf.name, 'rb')), save=False)
        tf.close()

    def save(self, *args, **kwargs):
        super(Photograph, self).save(*args, **kwargs)
        image = PImage.open(os.path.join(settings.MEDIA_ROOT, self.image.name))
        
        thumbnail_size = (250, 250)
        thumb_square = PImageOps.fit(image, thumbnail_size, PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        thumb_square.save(tf.name, image.format, quality=100)
        self.thumbnail_square.save(self.image.name, File(open(tf.name, 'rb')), save=False)
        tf.close()
      
        self.create_thumbnail(image, self.thumbnail_large, 1200)
        self.create_thumbnail(image, self.thumbnail_medium, 800)
        self.create_thumbnail(image, self.thumbnail_small, 300)

        super(Photograph, self).save(*args, **kwargs)

    def size(self):
        return '{width}x{height}'.format(width=self.width, height=self.height)

    def admin_thumbnail(self):
        if self.image:
            return '<img src="{url}" height="100" />'.format(url=self.thumbnail_small.url)
        else:
            return 'No image available'
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def __str__(self):
        return '{} ({}x{})'.format(self.title, self.width, self.height)


@receiver(post_delete, sender=Photograph)
def photograph_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.thumbnail_square.delete(False)
    instance.thumbnail_small.delete(False)
    instance.thumbnail_medium.delete(False)
    instance.thumbnail_large.delete(False)
