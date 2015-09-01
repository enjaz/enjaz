# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0015_assessment_cooperator_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='is_reviewed',
            field=models.BooleanField(default=True, verbose_name='\u0631\u0648\u062c\u0639\u062a\u061f'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='review_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644', blank=True),
        ),
    ]
