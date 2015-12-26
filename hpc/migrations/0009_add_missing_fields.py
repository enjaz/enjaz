# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0008_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 26, 8, 40, 4, 171570, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='code_name',
            field=models.CharField(default=b'', help_text='\u062d\u0631\u0648\u0641 \u0644\u0627\u062a\u064a\u0646\u064a\u0629 \u0635\u063a\u064a\u0631\u0629 \u0648\u0623\u0631\u0642\u0627\u0645', max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a'),
        ),
        migrations.AlterField(
            model_name='nonuser',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0637\u0627\u0644\u0628\u0629'), (b'M', '\u0637\u0627\u0644\u0628')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='gender',
            field=models.CharField(default=b'', max_length=1, choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0637\u0627\u0644\u0628\u0629'), (b'M', '\u0637\u0627\u0644\u0628')]),
        ),
    ]
