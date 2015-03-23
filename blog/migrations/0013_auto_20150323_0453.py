# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20150323_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='go_live_date',
            field=models.DateTimeField(verbose_name='Date and time to publish this post', default=datetime.datetime.now, blank=True, null=True),
            preserve_default=True,
        ),
    ]
