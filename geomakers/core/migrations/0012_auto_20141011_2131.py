# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_project_videos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['title']},
        ),
    ]
