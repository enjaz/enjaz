# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0006_fill_new_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='direct_entry',
            field=models.BooleanField(default=False),
        ),
    ]
