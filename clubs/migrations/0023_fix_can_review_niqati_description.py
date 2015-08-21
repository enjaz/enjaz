# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0022_club_can_review_niqati'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='can_review_niqati',
            field=models.BooleanField(default=False, verbose_name='\u064a\u0633\u062a\u0637\u064a\u0639 \u0645\u0631\u0627\u062c\u0639\u0629 \u0627\u0644\u0646\u0642\u0627\u0637\u061f'),
        ),
    ]
