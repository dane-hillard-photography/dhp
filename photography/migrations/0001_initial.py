# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import photography.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photograph',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('public', models.BooleanField(default=True)),
                ('orientation', models.CharField(editable=False, max_length=1, choices=[('P', 'Portrait'), ('L', 'Landscape'), ('S', 'Square')])),
                ('uuid', models.CharField(unique=True, editable=False, default=photography.models.generate_uuid, verbose_name='UUID', max_length=36)),
                ('published_date', models.DateTimeField(default=datetime.datetime.now)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('l_height', models.IntegerField(null=True, blank=True)),
                ('l_width', models.IntegerField(null=True, blank=True)),
                ('m_height', models.IntegerField(null=True, blank=True)),
                ('m_width', models.IntegerField(null=True, blank=True)),
                ('sm_height', models.IntegerField(null=True, blank=True)),
                ('sm_width', models.IntegerField(null=True, blank=True)),
                ('sq_height', models.IntegerField(null=True, blank=True)),
                ('sq_width', models.IntegerField(null=True, blank=True)),
                ('image', models.ImageField(width_field='width', upload_to=photography.models.get_file_path, height_field='height')),
                ('thumbnail_large', models.ImageField(null=True, width_field='l_width', upload_to='images/large', blank=True, height_field='l_height')),
                ('thumbnail_medium', models.ImageField(null=True, width_field='m_width', upload_to='images/medium', blank=True, height_field='m_height')),
                ('thumbnail_small', models.ImageField(null=True, width_field='sm_width', upload_to='images/small', blank=True, height_field='sm_height')),
                ('thumbnail_square', models.ImageField(null=True, width_field='sq_width', upload_to='images/square', blank=True, height_field='sq_height')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['-published_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoSet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=40)),
                ('body', models.TextField()),
                ('published_date', models.DateTimeField(default=datetime.datetime.now)),
                ('feature_photo', models.ForeignKey(related_name='photosets_featured_in', to='photography.Photograph')),
                ('photos', models.ManyToManyField(related_name='photosets_in', to='photography.Photograph')),
            ],
            options={
                'ordering': ['-published_date'],
            },
            bases=(models.Model,),
        ),
    ]
