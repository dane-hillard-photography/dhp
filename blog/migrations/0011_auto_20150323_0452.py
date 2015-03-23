# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20150323_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='go_live_date',
            field=models.DateTimeField(null=True, verbose_name='Date and time to publish this post', blank=True, default=datetime.datetime(2015, 3, 23, 4, 52, 41, 133520)),
            preserve_default=True,
        ),
    ]
