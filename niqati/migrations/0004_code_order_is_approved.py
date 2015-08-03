# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0003_auto_20150729_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='code_order',
            name='is_approved',
            field=models.NullBooleanField(default=None),
        ),
    ]
