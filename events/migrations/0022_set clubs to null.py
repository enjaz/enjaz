# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_Disscution Optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizing_club',
            field=models.ForeignKey(to='clubs.Club', null=True),
        ),
    ]
