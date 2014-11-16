# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='abstract',
            field=models.TextField(),
        ),
    ]
