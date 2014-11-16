# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_project_ratingasstring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ratingAsString',
            field=models.TextField(null=True, blank=True),
        ),
    ]
