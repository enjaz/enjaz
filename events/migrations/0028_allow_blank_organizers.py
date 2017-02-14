# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_rename_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizing_club',
            field=models.ForeignKey(blank=True, to='clubs.Club', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizing_team',
            field=models.ForeignKey(blank=True, to='clubs.Team', null=True),
        ),
    ]
