# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20150323_0408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='published',
        ),
        migrations.AlterField(
            model_name='post',
            name='go_live_date',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Date and time to publish this post', default=datetime.datetime(2015, 3, 23, 4, 30, 55, 12701)),
            preserve_default=True,
        ),
    ]
