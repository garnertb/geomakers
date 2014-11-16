# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_project_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='abstract',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='location',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
