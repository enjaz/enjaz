# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_tweet_media_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='failed_trials',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0627\u062a \u0627\u0644\u0641\u0627\u0634\u0644\u0629'),
        ),
    ]
