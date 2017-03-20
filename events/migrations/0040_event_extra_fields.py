# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0039_update_hpc_cirteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='evaluators_per_abstract',
            field=models.PositiveSmallIntegerField(default=2, null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0642\u064a\u0645\u064a\u0646 \u0648\u0627\u0644\u0645\u0642\u064a\u0645\u0627\u062a \u0644\u0643\u0644 \u0645\u0644\u062e\u0635 \u0628\u062d\u062b\u064a', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='notification_email',
            field=models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a \u0644\u0644\u062a\u0646\u0628\u064a\u0647\u0627\u062a', blank=True),
        ),
    ]
