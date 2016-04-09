# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_add_sfhcw_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location_url',
            field=models.URLField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.URLField(default=b'', max_length=255, blank=True),
        ),
    ]
