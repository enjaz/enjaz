# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0049_logo_path'),
        ('events', '0014_expand_abstract_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='abstract_revision_team',
            field=models.ForeignKey(related_name='abstract_revision_events', blank=True, to='clubs.Team', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='organizing_team',
            field=models.ForeignKey(to='clubs.Team', null=True),
        ),
    ]
