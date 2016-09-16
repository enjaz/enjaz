# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='media_path',
            field=models.CharField(default=b'', max_length=254, verbose_name='\u0645\u0633\u0627\u0631 \u0627\u0644\u0635\u0648\u0631\u0629 \u0627\u0644\u0645\u0631\u0641\u0642\u0629', blank=True),
        ),
    ]
