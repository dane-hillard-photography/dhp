import os
import uuid
from PIL import Image as PImage
from PIL import ImageOps as PImageOps
from tempfile import *

from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db.models import Max

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
    save_filename = "%s.%s" % (instance.uuid, ext)
    return os.path.join(instance.directory, save_filename)

class Album(models.Model):
    class Meta:
        ordering = ['sort_order']

    published_date = models.DateTimeField()
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    uuid = models.CharField("UUID", max_length=36, unique=True, default=generate_uuid, editable=False)
    sort_order = models.IntegerField(blank=True, null=True, default=max_sort_order)
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def photos(self):
        photo_list = ['<a href="%s">%s</a>' % (reverse('admin:photography_photograph_change', args=(photo.id,)), photo.title) for photo in self.photograph_set.all().reverse()]
        return ", ".join(photo_list)
    photos.allow_tags = True

    def get_absolute_url(self):
        return reverse('photography:album', kwargs={'album_id': self.uuid})

    def save(self, *args, **kwargs):
        current_order = 0
        new_order = 0

        if self.pk is not None:
            current = Album.objects.get(pk=self.pk)
            current_order = current.sort_order
            new_order = self.sort_order

        if current_order != new_order:
            existing_album = Album.objects.filter(sort_order=new_order)

            if existing_album:
                Album.objects.filter(pk=self.pk).update(sort_order=None)

                if current_order < new_order:
                    albums = Album.objects.filter(sort_order__gt=current_order, sort_order__lte=new_order)
                    for album in albums:
                        album.sort_order -= 1
                        super(Album, album).save()
                elif current_order > new_order:
                    albums = Album.objects.filter(sort_order__lt=current_order, sort_order__gte=new_order).reverse()
                    for album in albums:
                        album.sort_order += 1
                        super(Album, album).save()

        super(Album, self).save(*args, **kwargs)

class Tag(models.Model):
    class Meta:
        ordering = ['tag']

    tag = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.tag

class Photograph(models.Model):
    class Meta:
        ordering = ['-published_date']

    ORIENTATION_CHOICES = (
        ('P', 'Portrait'),
        ('L', 'Landscape'),
        ('S', 'Square'),
    )
  
    directory = "images/uncropped"

    published_date = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    album = models.ForeignKey(Album, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES, editable=False)
    uuid = models.CharField("UUID", max_length=36, unique=True, default=generate_uuid, editable=False)

    user = models.ForeignKey(User, blank=True, null=True)

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

    image = models.ImageField(upload_to=get_file_path, height_field="height", width_field="width")
    thumbnail_large = models.ImageField(upload_to="images/large", blank=True, null=True, height_field="l_height", width_field="l_width")
    thumbnail_medium = models.ImageField(upload_to="images/medium", blank=True, null=True, height_field="m_height", width_field="m_width")
    thumbnail_small = models.ImageField(upload_to="images/small", blank=True, null=True, height_field="sm_height", width_field="sm_width")
    thumbnail_square = models.ImageField(upload_to="images/square", blank=True, null=True, height_field="sq_height", width_field="sq_width")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('photography:photo', kwargs={'photo_id': self.uuid})

    def save(self, *args, **kwargs):
        super(Photograph, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        width, height = im.size
        ratio_divisor = height
        thumbnail_size = (200, 200)

        if width > height:
            self.orientation = "L"
            ratio_divisor = width
        elif width < height:
            self.orientation = "P"
        else:
            self.orientation = "S"
      
        ratio = 800.0 / ratio_divisor
        im.thumbnail((int(width * ratio), int(height * ratio)), PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        im.save(tf.name, im.format, quality=100)
        self.thumbnail_large.save(self.image.name, File(open(tf.name)), save=False)
        tf.close()

        ratio = 500.0 / ratio_divisor
        im.thumbnail((int(width * ratio), int(height * ratio)), PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        im.save(tf.name, im.format, quality=100)
        self.thumbnail_medium.save(self.image.name, File(open(tf.name)), save=False)
        tf.close()

        ratio = 200.0 / ratio_divisor
        im.thumbnail((int(width * ratio), int(height * ratio)), PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        im.save(tf.name, im.format, quality=100)
        self.thumbnail_small.save(self.image.name, File(open(tf.name)), save=False)
        tf.close()

        thumb_square = PImageOps.fit(im, thumbnail_size, PImage.ANTIALIAS)
        tf = NamedTemporaryFile()
        thumb_square.save(tf.name, im.format, quality=100)
        self.thumbnail_square.save(self.image.name, File(open(tf.name)), save=False)
        tf.close()

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

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __unicode__(self):
        return self.title
