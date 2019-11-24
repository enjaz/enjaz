# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_add_sorting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sorting',
            name='date_edited',
        ),
        migrations.AlterField(
            model_name='sorting',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of Sorting'),
        ),
        migrations.AlterField(
            model_name='sorting',
            name='sorting_score',
            field=models.IntegerField(verbose_name='Sorting Score Value'),
        ),
    ]
