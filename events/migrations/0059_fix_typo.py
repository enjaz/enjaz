# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0058_Add_Survie_to_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='mandotary_survey',
        ),
        migrations.AddField(
            model_name='session',
            name='mandatory_survey',
            field=models.ForeignKey(related_name='mandatory_sessions', blank=True, to='events.Survey', null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='optional_survey',
            field=models.ForeignKey(related_name='optional_sessions', blank=True, to='events.Survey', null=True),
        ),
    ]
