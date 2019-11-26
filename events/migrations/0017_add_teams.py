# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0055_add_2019_2020_clubs'),
        ('events', '0016_add_why_deleted_abstract'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='evaluating_team',
            field=models.ForeignKey(related_name='evaluating_team_events', verbose_name='\u0644\u062c\u0646\u0629 \u062a\u0642\u064a\u064a\u0645 \u0627\u0644\u0623\u0628\u062d\u0627\u062b', blank=True, to='clubs.Team', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='oral_poster_team',
            field=models.ForeignKey(related_name='oralposter_team_events', verbose_name='\u0644\u062c\u0646\u0629 \u0627\u0644\u0639\u0631\u0648\u0636 \u0648\u0627\u0644\u0645\u0644\u0635\u0642\u0627\u062a \u0627\u0644\u0628\u062d\u062b\u064a\u0629', blank=True, to='clubs.Team', null=True),
        ),
    ]
