# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_years'),
        ('clubs', '0010_add_missing_colleges'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='core.StudentClubYear', null=True, verbose_name='\u0627\u0644\u0633\u0646\u0629'),
        ),
    ]
