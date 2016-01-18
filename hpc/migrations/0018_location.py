# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0017_registration_moved_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='date',
            field=models.DateField(null=True, verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e'),
        ),
        migrations.AddField(
            model_name='session',
            name='end_time',
            field=models.TimeField(default=None, null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='location',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646', blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='start_time',
            field=models.TimeField(default=None, null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629', blank=True),
        ),
    ]
