# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0050_event_sends_badges_automatically'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionregistration',
            name='badge_sent',
            field=models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0627\u0644\u0628\u0637\u0627\u0642\u0629\u061f'),
        ),
    ]
