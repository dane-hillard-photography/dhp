# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_meta_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='meta_description',
            field=models.CharField(null=True, max_length=150, blank=True),
        ),
    ]
