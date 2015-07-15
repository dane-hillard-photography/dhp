# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import photography.models


class Migration(migrations.Migration):

    replaces = [('photography', '0001_initial'), ('photography', '0002_auto_20150628_2036'), ('photography', '0003_remove_photograph_orientation')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photograph',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('public', models.BooleanField(default=True)),
                ('uuid', models.CharField(editable=False, verbose_name='UUID', default=photography.models.generate_uuid, max_length=36, unique=True)),
                ('published_date', models.DateTimeField(default=datetime.datetime.now)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('l_height', models.IntegerField(blank=True, null=True)),
                ('l_width', models.IntegerField(blank=True, null=True)),
                ('m_height', models.IntegerField(blank=True, null=True)),
                ('m_width', models.IntegerField(blank=True, null=True)),
                ('sm_height', models.IntegerField(blank=True, null=True)),
                ('sm_width', models.IntegerField(blank=True, null=True)),
                ('sq_height', models.IntegerField(blank=True, null=True)),
                ('sq_width', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(width_field='width', height_field='height', upload_to=photography.models.get_file_path)),
                ('thumbnail_large', models.ImageField(width_field='l_width', upload_to='images/large', height_field='l_height', null=True, blank=True)),
                ('thumbnail_medium', models.ImageField(width_field='m_width', upload_to='images/medium', height_field='m_height', null=True, blank=True)),
                ('thumbnail_small', models.ImageField(width_field='sm_width', upload_to='images/small', height_field='sm_height', null=True, blank=True)),
                ('thumbnail_square', models.ImageField(width_field='sq_width', upload_to='images/square', height_field='sq_height', null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'ordering': ['-published_date'],
            },
        ),
    ]
