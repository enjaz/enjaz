# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0020_registration_reminder_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='for_onsite_registration',
            field=models.BooleanField(default=False, verbose_name='\u0645\u062a\u0627\u062d \u0627\u0644\u062a\u0633\u062c\u064a\u0644 \u0641\u064a \u064a\u0648\u0645 \u0627\u0644\u062d\u062f\u062b\u061f'),
        ),
    ]
