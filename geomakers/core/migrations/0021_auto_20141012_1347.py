# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20141012_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('facebook', models.URLField(default=b'', null=True, blank=True)),
                ('twitter', models.URLField(default=b'', null=True, blank=True)),
                ('linkedin', models.URLField(default=b'', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
