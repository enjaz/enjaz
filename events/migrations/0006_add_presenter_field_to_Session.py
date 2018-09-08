# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_add_fields_to_events_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='presenter',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
