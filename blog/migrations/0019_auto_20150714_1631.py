# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20150713_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='related_links',
            field=models.ManyToManyField(blank=True, to='blog.Link'),
        ),
    ]
