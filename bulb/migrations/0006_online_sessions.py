# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0005_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='\u062c\u0644\u0633\u0629 \u0627\u0644\u0625\u0646\u062a\u0631\u0646\u062a\u061f'),
        ),
        migrations.AlterField(
            model_name='group',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629 \u0645\u0648\u062c\u0651\u0647\u0629 \u0625\u0644\u0649', blank=True, choices=[(b'', '\u0627\u0644\u0637\u0644\u0627\u0628 \u0648\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a'), (b'F', '\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0627\u0644\u0637\u0644\u0627\u0628')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='location',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646', blank=True),
        ),
    ]
