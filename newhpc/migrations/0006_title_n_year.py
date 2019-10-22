# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newhpc', '0004_unicode_n_edu_lvl_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='hpcleader',
            name='arabic_title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='previousversion',
            name='year',
            field=models.CharField(default=b'', max_length=4, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb3\xd9\x86\xd8\xa9'),
        ),
    ]
