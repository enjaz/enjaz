# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0039_fill_can_submit_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='can_skip_followup_reports',
            field=models.BooleanField(default=False, verbose_name='\u064a\u0633\u062a\u0637\u064a\u0639 \u062a\u062c\u0627\u0648\u0632 \u0627\u0644\u062a\u0642\u0627\u0631\u064a\u0631 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a\u0629\u061f'),
        ),
    ]
