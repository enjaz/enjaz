# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20191018_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstract',
            name='was_presented_at_conference',
            field=models.CharField(default=b'N', max_length=1, verbose_name=b'Has the study been presented in a conference before?', choices=[(b'N', b'No'), (b'Y', b'Yes')]),
        ),
    ]
