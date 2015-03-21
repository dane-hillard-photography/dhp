# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photography', '0001_initial'),
        ('blog', '0005_auto_20150320_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='feature_image',
            field=models.ForeignKey(to='photography.Photograph', blank=True, null=True),
            preserve_default=True,
        ),
    ]
