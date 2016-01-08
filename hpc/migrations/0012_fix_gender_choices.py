# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0011_allow_blank_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonuser',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', choices=[(b'F', '\u0637\u0627\u0644\u0628\u0629'), (b'M', '\u0637\u0627\u0644\u0628')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='gender',
            field=models.CharField(default=b'', max_length=1, blank=True, choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')]),
        ),
    ]
