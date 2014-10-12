# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skyshaker', '0010_auto_20141011_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='videos',
            field=models.ManyToManyField(to='skyshaker.Video', blank=True),
            preserve_default=True,
        ),
    ]
