# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0013_add_2015_clubs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', blank=True, choices=[(b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')]),
        ),
    ]
