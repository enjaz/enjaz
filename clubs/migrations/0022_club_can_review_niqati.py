# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0021_add_jeddah_ahsa_deanships'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='can_review_niqati',
            field=models.BooleanField(default=False, verbose_name='\u064a\u0633\u062a\u0637\u064a\u0639 \u0627\u0644\u062a\u0639\u062f\u064a\u0644\u061f'),
        ),
    ]
