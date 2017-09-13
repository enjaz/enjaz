# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0004_auto_20170913_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityrequest',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 9, 13, 3, 8, 34, 492291, tzinfo=utc), verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0647\u0627\u064a\u0629'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='location',
            field=models.CharField(default='', max_length=100, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2017, 9, 13, 3, 8, 43, 747134, tzinfo=utc), verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0628\u062f\u0627\u064a\u0629'),
            preserve_default=False,
        ),
    ]
