# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0029_gender_for_presidencies'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='can_view_assessments',
            field=models.BooleanField(default=False, verbose_name='\u064a\u0633\u062a\u0637\u064a\u0639 \u0645\u0634\u0627\u0647\u062f\u0629 \u062a\u0642\u064a\u064a\u0645\u0627\u062a \u0627\u0644\u0623\u0646\u0634\u0637\u0629\u061f'),
        ),
    ]
