import os
import logging
from tempfile import NamedTemporaryFile

from PIL import Image as PImage

from django.db import models
from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_delete
from django.core.files.move import file_move_safe
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)

IMAGE_SUBPATH = 'images'
ORIG_SUBPATH = os.path.join(IMAGE_SUBPATH, 'uncropped')
LARGE_SUBPATH = os.path.join(IMAGE_SUBPATH, 'large')
MEDIUM_SUBPATH = os.path.join(IMAGE_SUBPATH, 'medium')
SMALL_SUBPATH = os.path.join(IMAGE_SUBPATH, 'small')


def generate_uuid():
    pass


def get_file_path(instance, filename):
    return os.path.join(ORIG_SUBPATH, filename)


class Photograph(models.Model):

    alt_text = models.CharField(max_length=255)
    filename = models.CharField(max_length=100, blank=True, null=True)
    in_portfolio = models.BooleanField(default=False)

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
        upload_to=LARGE_SUBPATH, blank=True, null=True, height_field='l_height', width_field='l_width')
    thumbnail_medium = models.ImageField(
        upload_to=MEDIUM_SUBPATH, blank=True, null=True, height_field='m_height', width_field='m_width')
    thumbnail_small = models.ImageField(
        upload_to=SMALL_SUBPATH, blank=True, null=True, height_field='sm_height', width_field='sm_width')

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

    def clean(self):
        super(Photograph, self).clean()
        new_filepath = os.path.join(settings.MEDIA_ROOT, ORIG_SUBPATH, self.filename)
        existing_filepath = None
        existing_filename = None

        if self.pk:
            existing_photo = Photograph.objects.get(pk=self.pk)
            existing_filepath = existing_photo.image.path
            existing_filename = existing_photo.filename

        if self.pk is None or (self.filename and new_filepath != existing_filepath):
            if os.path.isfile(new_filepath):
                raise ValidationError({'filename': 'A photo with this filename already exists!'})
        if existing_filename and not self.filename:
            raise ValidationError({'filename': 'Don\'t orphan an otherwise happy photo!'})

    def save(self, *args, **kwargs):
        self.clean()
        super(Photograph, self).save(*args, **kwargs)

        image = PImage.open(os.path.join(settings.MEDIA_ROOT, self.image.name))

        self.create_thumbnail(image, self.thumbnail_large, 1200)
        self.create_thumbnail(image, self.thumbnail_medium, 800)
        self.create_thumbnail(image, self.thumbnail_small, 300)

        for img in [self.image, self.thumbnail_large, self.thumbnail_medium, self.thumbnail_small]:
            if self.filename:
                file_move_safe(
                    img.path,
                    os.path.join(os.path.dirname(img.path), self.filename)
                )
                img.name = os.path.join(os.path.dirname(img.name), self.filename)

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
        return '{} ({}x{})'.format(self.alt_text, self.width, self.height)


@receiver(post_delete, sender=Photograph)
def photograph_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.thumbnail_small.delete(False)
    instance.thumbnail_medium.delete(False)
    instance.thumbnail_large.delete(False)
