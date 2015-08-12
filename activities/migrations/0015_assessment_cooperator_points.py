# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0014_add_criteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='cooperator_points',
            field=models.IntegerField(default=0, verbose_name='\u0646\u0642\u0627\u0637 \u0627\u0644\u062a\u0639\u0627\u0648\u0646'),
        ),
    ]
