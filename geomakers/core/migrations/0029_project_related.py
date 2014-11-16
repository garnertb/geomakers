# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20141012_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='related',
            field=models.ManyToManyField(related_name='related_rel_+', to='core.Project', blank=True),
            preserve_default=True,
        ),
    ]
