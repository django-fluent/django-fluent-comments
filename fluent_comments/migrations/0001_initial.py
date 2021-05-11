# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("django_comments", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="FluentComment",
            fields=[],
            options={
                "managed": False,
                "proxy": True,
                "managed": False,
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
            bases=("django_comments.comment",),
        ),
    ]
