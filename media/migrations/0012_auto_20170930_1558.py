# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0011_auto_20170930_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snapchatreservation',
            old_name='pup_date',
            new_name='submission_datetime',
        ),
        migrations.AlterField(
            model_name='snapchatreservation',
            name='end_time',
            field=models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629'),
        ),
        migrations.AlterField(
            model_name='snapchatreservation',
            name='start_time',
            field=models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629'),
        ),
    ]
