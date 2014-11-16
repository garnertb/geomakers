# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='images',
            field=models.ManyToManyField(to='core.Image', blank=True),
            preserve_default=True,
        ),
    ]
