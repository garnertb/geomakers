# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_project_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='link',
            new_name='url',
        ),
        migrations.AddField(
            model_name='link',
            name='title',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='links',
            field=models.ManyToManyField(to='core.Link', blank=True),
            preserve_default=True,
        ),
    ]
