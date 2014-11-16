# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='MakerSpace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('lat', models.DecimalField(max_digits=8, decimal_places=5)),
                ('lon', models.DecimalField(max_digits=8, decimal_places=5)),
                ('url', models.URLField(default=b'', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
