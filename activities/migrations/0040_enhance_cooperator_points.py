# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0039_blank_criteria_instructions'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='has_shared_points',
            field=models.BooleanField(default=False, verbose_name='\u0646\u0642\u0627\u0637 \u0627\u0644\u062a\u0642\u064a\u064a\u0645 \u0645\u062a\u0642\u0627\u0633\u0645\u0629\u061f'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='cooperator_points',
            field=models.FloatField(default=0, verbose_name='\u0646\u0642\u0627\u0637 \u0627\u0644\u062a\u0639\u0627\u0648\u0646'),
        ),
        migrations.AlterField(
            model_name='criterion',
            name='category',
            field=models.CharField(max_length=1, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641', choices=[(b'P', '\u0631\u0626\u0627\u0633\u0629 \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628'), (b'M', '\u0627\u0644\u0645\u0631\u0643\u0632 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a')]),
        ),
    ]
