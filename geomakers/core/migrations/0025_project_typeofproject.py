# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_userprofile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='typeOfProject',
            field=models.CharField(blank=True, max_length=200, null=True, choices=[(b'GeoDream', b'GeoDream'), (b'GeoRecipe', b'GeoRecipe'), (b'GeoBoost', b'GeoBoost')]),
            preserve_default=True,
        ),
    ]
