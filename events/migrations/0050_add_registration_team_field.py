# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0052_presidencies_can_assess'),
        ('events', '0049_event_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_team',
            field=models.ForeignKey(related_name='registration_team_events', verbose_name='\u0641\u0631\u064a\u0642 \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True, to='clubs.Team', null=True),
        ),
    ]
