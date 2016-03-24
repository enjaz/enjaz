# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_add_focr_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_on_telegram',
            field=models.BooleanField(default=True, verbose_name='\u0645\u062a\u0627\u062d \u0627\u0644\u062a\u0633\u062c\u064a\u0644 \u0641\u064a \u064a\u0648\u0645 \u0627\u0644\u062d\u062f\u062b\u061f'),
        ),
        migrations.AddField(
            model_name='event',
            name='twitter',
            field=models.CharField(default=b'KSAU_Events', max_length=255, blank=True),
        ),
    ]
