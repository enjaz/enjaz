# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0052_presidencies_can_assess'),
        ('events', '0045_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='abstract_revision_club',
        ),
        migrations.RemoveField(
            model_name='event',
            name='organizing_club',
        ),
        migrations.AddField(
            model_name='event',
            name='attendance_team',
            field=models.ForeignKey(related_name='attendance_team_events', verbose_name='\u0641\u0631\u064a\u0642 \u0627\u0644\u062a\u062d\u0636\u064a\u0631', blank=True, to='clubs.Team', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='has_attendance',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u064a\u0633\u062a\u062e\u062f\u0645 \u0627\u0644\u062d\u062f\u062b \u0646\u0638\u0627\u0645 \u0627\u0644\u062a\u062d\u0636\u064a\u0631\u061f'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizing_team',
            field=models.ForeignKey(verbose_name='\u0641\u0631\u064a\u0642 \u0627\u0644\u062a\u0646\u0638\u064a\u0645', blank=True, to='clubs.Team', null=True),
        ),
    ]
