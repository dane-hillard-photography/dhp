# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='go_live_date',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Date and time to publish this post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='take_down_date',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Date and time to unpublish this post'),
            preserve_default=True,
        ),
    ]
