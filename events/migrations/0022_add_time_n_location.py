# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_add_new_who_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='presentaion_location',
            field=models.CharField(max_length=300, null=True, verbose_name='\u0645\u0643\u0627\u0646 \u0627\u0644\u0639\u0631\u0636', blank=True),
        ),
        migrations.AddField(
            model_name='abstract',
            name='presentaion_time',
            field=models.TimeField(null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0639\u0631\u0636', blank=True),
        ),
    ]
