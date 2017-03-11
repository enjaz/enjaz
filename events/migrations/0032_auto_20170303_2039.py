# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0031_event_hashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='time_slot',
            field=models.ForeignKey(blank=True, to='events.TimeSlot', null=True),
        ),
    ]
