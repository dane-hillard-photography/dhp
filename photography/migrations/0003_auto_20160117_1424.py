# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-17 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photography', '0002_auto_20160114_1613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photograph',
            old_name='title',
            new_name='alt_text',
        ),
        migrations.RemoveField(
            model_name='photograph',
            name='description',
        ),
    ]