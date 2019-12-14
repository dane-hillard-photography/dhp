# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ("photography", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, primary_key=True, auto_created=True)),
                ("name", models.CharField(unique=True, max_length=255)),
            ],
            options={"verbose_name_plural": "categories",},
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, primary_key=True, auto_created=True)),
                ("title", models.CharField(max_length=255)),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, primary_key=True, auto_created=True)),
                ("title", models.CharField(unique=True, max_length=255)),
                ("slug", models.SlugField(unique=True, max_length=255)),
                ("subtitle", models.CharField(null=True, blank=True, max_length=255)),
                ("body", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "go_live_date",
                    models.DateTimeField(
                        null=True,
                        blank=True,
                        verbose_name="Date and time to publish this post",
                        default=datetime.datetime.now,
                    ),
                ),
                (
                    "take_down_date",
                    models.DateTimeField(null=True, blank=True, verbose_name="Date and time to unpublish this post"),
                ),
                ("categories", models.ManyToManyField(to="blog.Category", blank=True)),
                (
                    "feature_image",
                    models.ForeignKey(to="photography.Photograph", null=True, blank=True, on_delete=models.SET_NULL),
                ),
                ("related_links", models.ManyToManyField(to="blog.Link", blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, primary_key=True, auto_created=True)),
                ("name", models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(model_name="post", name="tags", field=models.ManyToManyField(to="blog.Tag", blank=True),),
    ]
