# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching_program', '0008_auto_20180303_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchproject',
            name='status',
            field=models.CharField(default=b'Applied', max_length=10, choices=[(b'Applied', b'applied'), (b'New', b'new'), (b'In Progress', b'in progress'), (b'Puplished', b'puplished')]),
        ),
        migrations.RemoveField(
            model_name='studentapplication',
            name='skills',
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='skills',
            field=models.CharField(default='old', max_length=255),
            preserve_default=False,
        ),
    ]
