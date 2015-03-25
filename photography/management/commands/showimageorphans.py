import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from photography.models import Photograph

IMAGES_PATH = os.path.join(settings.MEDIA_ROOT, 'images')


class Command(BaseCommand):
    help = 'Removes images that are no longer referenced by a Photograph instance'

    def handle(self, *args, **kwargs):
        referenced_images = []

        for photograph in Photograph.objects.all():
            referenced_images.append(os.path.basename(photograph.image.name))

        for root, dirs, files in os.walk(IMAGES_PATH):
            if root != IMAGES_PATH:
                unused_images = [os.path.join(root, file) for file in files if file not in referenced_images]
                if unused_images:
                    print('\n'.join(unused_images))
