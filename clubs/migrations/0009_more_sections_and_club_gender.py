# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0008_add_city_colleges'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', blank=True, choices=[(b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')]),
        ),
        migrations.AlterField(
            model_name='college',
            name='section',
            field=models.CharField(max_length=2, verbose_name='\u0627\u0644\u0642\u0633\u0645', choices=[(b'NG', '\u0627\u0644\u062d\u0631\u0633 \u0627\u0644\u0648\u0637\u0646\u064a'), (b'KF', '\u0645\u062f\u064a\u0646\u0629 \u0627\u0644\u0645\u0644\u0643 \u0641\u0647\u062f \u0627\u0644\u0637\u0628\u064a\u0629'), (b'J', '\u062c\u062f\u0629'), (b'A', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')]),
        ),
    ]
