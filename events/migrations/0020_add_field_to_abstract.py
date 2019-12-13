# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_add_highest_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='is_statistically_excluded',
            field=models.BooleanField(default=False),
        ),
    ]
