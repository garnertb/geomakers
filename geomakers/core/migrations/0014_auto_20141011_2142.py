# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_link_embed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='embed',
        ),
        migrations.AddField(
            model_name='video',
            name='embed',
            field=models.TextField(default=b'', null=True, blank=True),
            preserve_default=True,
        ),
    ]
