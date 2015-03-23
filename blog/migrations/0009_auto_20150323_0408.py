# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20150323_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='go_live_date',
            field=models.DateTimeField(null=True, blank=True, default=datetime.datetime(2015, 3, 23, 4, 8, 12, 11211), verbose_name='Date and time to publish this post'),
            preserve_default=True,
        ),
    ]
