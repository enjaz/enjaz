# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0035_add_public_health_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='is_assessed',
            field=models.BooleanField(default=True, verbose_name='\u0647\u0644 \u064a\u062e\u0636\u0639 \u0644\u0644\u062a\u0642\u064a\u064a\u0645\u061f'),
        ),
    ]
