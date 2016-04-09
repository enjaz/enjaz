# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_add_location_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='first_priority_sessions',
            field=models.ManyToManyField(related_name='first_priority_registrations', to='events.Session', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='second_priority_sessions',
            field=models.ManyToManyField(related_name='second_priority_registrations', to='events.Session', blank=True),
        ),
    ]
