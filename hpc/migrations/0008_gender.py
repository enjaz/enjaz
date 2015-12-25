# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0007_add_hpc_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonuser',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', choices=[(b'F', b'\xd8\xb7\xd8\xa7\xd9\x84\xd8\xa8\xd8\xa9'), (b'M', b'\xd8\xb7\xd8\xa7\xd9\x84\xd8\xa8')]),
        ),
        migrations.AlterField(
            model_name='nonuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a'),
        ),
        migrations.AlterField(
            model_name='session',
            name='gender',
            field=models.CharField(default=b'', max_length=1, choices=[(b'F', b'\xd8\xb7\xd8\xa7\xd9\x84\xd8\xa8\xd8\xa9'), (b'M', b'\xd8\xb7\xd8\xa7\xd9\x84\xd8\xa8')]),
        ),
    ]
