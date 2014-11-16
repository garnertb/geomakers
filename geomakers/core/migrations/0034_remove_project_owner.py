# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20141021_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
    ]
