# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photography', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photoset',
            name='feature_photo',
        ),
        migrations.RemoveField(
            model_name='photoset',
            name='photos',
        ),
        migrations.DeleteModel(
            name='PhotoSet',
        ),
    ]
