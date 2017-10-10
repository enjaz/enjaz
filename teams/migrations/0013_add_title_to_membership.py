# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_add_title_to_postion'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='title',
            field=models.CharField(max_length=50, verbose_name='\u0627\u0644\u0645\u0646\u0635\u0628', blank=True),
        ),
    ]
