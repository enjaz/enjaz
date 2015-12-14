# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='level',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'Level', choices=[(b'U', b'Undergraduate'), (b'G', b'Graduate')]),
        ),
    ]
