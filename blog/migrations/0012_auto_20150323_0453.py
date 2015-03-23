# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20150323_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='go_live_date',
            field=models.DateTimeField(blank=True, verbose_name='Date and time to publish this post', null=True, default=datetime.datetime(2015, 3, 23, 4, 53, 24, 380253)),
            preserve_default=True,
        ),
    ]
