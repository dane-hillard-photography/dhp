# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime
import photography.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Photograph",
            fields=[
                ("id", models.AutoField(serialize=False, primary_key=True, verbose_name="ID", auto_created=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(null=True, blank=True)),
                ("public", models.BooleanField(default=True)),
                (
                    "uuid",
                    models.CharField(
                        editable=False,
                        verbose_name="UUID",
                        max_length=36,
                        unique=True,
                        default=photography.models.generate_uuid,
                    ),
                ),
                ("published_date", models.DateTimeField(default=datetime.datetime.now)),
                ("height", models.IntegerField(null=True, blank=True)),
                ("width", models.IntegerField(null=True, blank=True)),
                ("l_height", models.IntegerField(null=True, blank=True)),
                ("l_width", models.IntegerField(null=True, blank=True)),
                ("m_height", models.IntegerField(null=True, blank=True)),
                ("m_width", models.IntegerField(null=True, blank=True)),
                ("sm_height", models.IntegerField(null=True, blank=True)),
                ("sm_width", models.IntegerField(null=True, blank=True)),
                ("sq_height", models.IntegerField(null=True, blank=True)),
                ("sq_width", models.IntegerField(null=True, blank=True)),
                (
                    "image",
                    models.ImageField(
                        width_field="width", upload_to=photography.models.get_file_path, height_field="height"
                    ),
                ),
                (
                    "thumbnail_large",
                    models.ImageField(
                        width_field="l_width", upload_to="images/large", null=True, height_field="l_height", blank=True
                    ),
                ),
                (
                    "thumbnail_medium",
                    models.ImageField(
                        width_field="m_width", upload_to="images/medium", null=True, height_field="m_height", blank=True
                    ),
                ),
                (
                    "thumbnail_small",
                    models.ImageField(
                        width_field="sm_width",
                        upload_to="images/small",
                        null=True,
                        height_field="sm_height",
                        blank=True,
                    ),
                ),
                (
                    "thumbnail_square",
                    models.ImageField(
                        width_field="sq_width",
                        upload_to="images/square",
                        null=True,
                        height_field="sq_height",
                        blank=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
                ),
            ],
            options={"ordering": ["-published_date"],},
        ),
    ]
