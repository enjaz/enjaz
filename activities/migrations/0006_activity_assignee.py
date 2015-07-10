# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0014_fix_gender_verbose_name'),
        ('activities', '0005_activity_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='assignee',
            field=models.ForeignKey(related_name='assigned_activities', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0645\u0633\u0646\u062f', to='clubs.Club', null=True),
        ),
    ]
