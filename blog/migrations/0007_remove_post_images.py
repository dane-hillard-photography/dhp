# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-19 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_auto_20160119_1844"),
    ]

    operations = [
        migrations.RemoveField(model_name="post", name="images",),
    ]
