# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skyshaker', '0018_project_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ratingAsString',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
