# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0037_fill_is_assessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='can_submit_activities',
            field=models.BooleanField(default=True, verbose_name='\u0647\u0644 \u064a\u0633\u062a\u0637\u064a\u0639 \u0631\u0641\u0639 \u0623\u0646\u0634\u0637\u0629\u061f'),
        ),
    ]
