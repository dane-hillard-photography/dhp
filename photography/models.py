import os
import logging
from io import BytesIO
from tempfile import NamedTemporaryFile

from PIL import Image as PImage

from django.core.files.storage import default_storage
from django.db import models
from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_delete
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe

LOGGER = logging.getLogger(__name__)

IMAGE_SUBPATH = 'images'
ORIG_SUBPATH = os.path.join(IMAGE_SUBPATH, 'uncropped')
LARGE_SUBPATH = os.path.join(IMAGE_SUBPATH, 'large')
MEDIUM_SUBPATH = os.path.join(IMAGE_SUBPATH, 'medium')
SMALL_SUBPATH = os.path.join(IMAGE_SUBPATH, 'small')


def generate_uuid():
    pass


def get_file_path(instance, filename):
    return os.path.join(ORIG_SUBPATH, instance.filename)


def create_thumbnail(original_image, new_image, new_image_filename, max_size):
    width, height = original_image.size
    ratio_divisor = height if height > width else width
    ratio = float(max_size) / ratio_divisor

    original_image.thumbnail((int(width * ratio), int(height * ratio)), PImage.ANTIALIAS)
    tf = NamedTemporaryFile()
    original_image.save(tf.name, original_image.format, quality=100)
    new_image.save(new_image_filename, File(open(tf.name, 'rb')), save=False)
    tf.close()


def clean_up_thumbnails(filename):
    for size in (LARGE_SUBPATH, MEDIUM_SUBPATH, SMALL_SUBPATH):
        default_storage.delete(os.path.join(settings.MEDIA_ROOT, size, filename))


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

    image = models.ImageField(
        upload_to=get_file_path,
        height_field='height',
        width_field='width'
    )

    thumbnail_large = models.ImageField(
        upload_to=LARGE_SUBPATH,
        blank=True,
        null=True,
        height_field='l_height',
        width_field='l_width'
    )

    thumbnail_medium = models.ImageField(
        upload_to=MEDIUM_SUBPATH,
        blank=True,
        null=True,
        height_field='m_height',
        width_field='m_width'
    )

    thumbnail_small = models.ImageField(
        upload_to=SMALL_SUBPATH,
        blank=True,
        null=True,
        height_field='sm_height',
        width_field='sm_width'
    )

    def get_absolute_url(self):
        return reverse('photography:photo', kwargs={'photo_id': self.uuid})

    def clean(self):
        super(Photograph, self).clean()

        try:
            photo_using_this_filename = Photograph.objects.get(filename=self.filename)
        except Photograph.DoesNotExist:
            pass
        else:
            if photo_using_this_filename and photo_using_this_filename.pk != self.pk:
                raise ValidationError({
                    'filename': 'Another photo is using this filename already. Please choose another!'
                })

        if self.pk and not self.filename:
            raise ValidationError({
                'filename': 'Every photo must have a filename.'
            })

    def save(self, *args, **kwargs):
        self.clean()
        create_thumbnails = True
        current_file_path = os.path.join(settings.MEDIA_ROOT, ORIG_SUBPATH, self.filename)

        if self.pk:
            previously_set_filename = Photograph.objects.get(pk=self.pk).filename
            previously_set_file_path = os.path.join(settings.MEDIA_ROOT, ORIG_SUBPATH, previously_set_filename)

            if self.filename != previously_set_filename:
                LOGGER.info(f'Getting contents from {previously_set_filename}')
                previous_file = default_storage.open(previously_set_file_path)

                LOGGER.info(f'Writing contents to {current_file_path}')
                self.image.save(current_file_path, previous_file, save=False)

                previous_file.close()

                LOGGER.info('Deleting existing thumbnails')
                clean_up_thumbnails(previously_set_filename)

                LOGGER.info('Deleting previous original image')
                default_storage.delete(previously_set_file_path)
            else:
                create_thumbnails = False

        self.image.name = current_file_path

        super(Photograph, self).save(*args, **kwargs)

        LOGGER.info(f'Reading {self.filename} for thumbnailing...')
        image = PImage.open(default_storage.open(current_file_path))

        if create_thumbnails:
            LOGGER.info('Creating thumbnails')
            create_thumbnail(image, self.thumbnail_large, self.filename, 1200)
            create_thumbnail(image, self.thumbnail_medium, self.filename, 800)
            create_thumbnail(image, self.thumbnail_small, self.filename, 300)

        super(Photograph, self).save(*args, **kwargs)

    def size(self):
        return '{width}x{height}'.format(width=self.width, height=self.height)

    def admin_thumbnail(self):
        if self.image:
            return mark_safe('<img src="{url}" height="100" />'.format(url=self.thumbnail_small.url))
        else:
            return 'No image available'
    admin_thumbnail.short_description = 'Thumbnail'

    def __str__(self):
        return '{} ({}x{})'.format(self.alt_text, self.width, self.height)


@receiver(post_delete, sender=Photograph)
def photograph_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.thumbnail_small.delete(False)
    instance.thumbnail_medium.delete(False)
    instance.thumbnail_large.delete(False)
