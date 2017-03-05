# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_add_hpc2_programs'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='twitter_event_name',
            field=models.CharField(default=b'', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0641\u064a \u062a\u063a\u0631\u064a\u062f\u0629 \u062a\u0648\u064a\u062a\u0631', blank=True),
        ),
    ]
