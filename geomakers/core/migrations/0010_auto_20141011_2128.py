# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20141011_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
