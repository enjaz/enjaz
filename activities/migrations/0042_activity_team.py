# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_merge'),
        ('activities', '0041_add_jeddah_criteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='team',
            field=models.ForeignKey(related_name='old_activities', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0641\u0631\u064a\u0642 \u0627\u0644\u0645\u0646\u0638\u0651\u0645', to='teams.Team', null=True),
        ),
    ]
