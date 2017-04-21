# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0049_event_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sends_badges_automatically',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u062a\u0631\u0633\u0644 \u0627\u0644\u0628\u0637\u0627\u0642\u0627\u062a \u0628\u0634\u0643\u0644 \u0622\u0644\u064a \u0644\u0644\u0645\u0633\u062c\u0644\u064a\u0646 \u0648\u0627\u0644\u0645\u0633\u062c\u0644\u0627\u062a \u062d\u062f\u064a\u062b\u0627\u061f'),
        ),
    ]
