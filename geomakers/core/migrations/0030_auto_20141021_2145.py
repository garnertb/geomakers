# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_project_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='rating',
            field=models.IntegerField(default=b'3', null=True, blank=True),
        ),
    ]
