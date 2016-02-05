# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_clearer_badge_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonprofile',
            name='modification_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
