# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    replaces = [('blog', '0001_initial'), ('blog', '0002_auto_20150320_0120'), ('blog', '0003_auto_20150320_0127'), ('blog', '0004_auto_20150320_0130'), ('blog', '0005_auto_20150320_0131'), ('blog', '0006_post_feature_image'), ('blog', '0007_post_subtitle'), ('blog', '0008_auto_20150323_0406'), ('blog', '0009_auto_20150323_0408'), ('blog', '0010_auto_20150323_0430'), ('blog', '0011_auto_20150323_0452'), ('blog', '0012_auto_20150323_0453'), ('blog', '0013_auto_20150323_0453'), ('blog', '0014_auto_20150628_2036'), ('blog', '0014_auto_20150618_1718'), ('blog', '0015_merge'), ('blog', '0016_auto_20150628_2140'), ('blog', '0017_auto_20150628_2140'), ('blog', '0018_auto_20150713_1945'), ('blog', '0019_auto_20150714_1631')]

    dependencies = [
        ('photography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('body', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, to='blog.Category'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='feature_image',
            field=models.ForeignKey(to='photography.Photograph', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='post',
            name='go_live_date',
            field=models.DateTimeField(null=True, default=datetime.datetime.now, blank=True, verbose_name='Date and time to publish this post'),
        ),
        migrations.AddField(
            model_name='post',
            name='take_down_date',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Date and time to unpublish this post'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='published',
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='related_links',
            field=models.ManyToManyField(blank=True, to='blog.Link'),
        ),
    ]
