# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_merge'),
        ('bulb', '0033_auto_20171006_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruitment',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True),
        ),
    ]
