# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0038_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='instructions',
            field=models.TextField(verbose_name='\u062a\u0639\u0644\u064a\u0645\u0627\u062a', blank=True),
        ),
    ]
