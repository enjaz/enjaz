# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_add_twitter_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_auto_tweet',
            field=models.BooleanField(default=True, verbose_name='\u062a\u063a\u0631\u064a\u062f \u062a\u0644\u0642\u0627\u0626\u064a\u061f'),
        ),
    ]
