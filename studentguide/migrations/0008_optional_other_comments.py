# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0007_add_assessor_improve_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='other_comments',
            field=models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0623\u062e\u0631\u0649', blank=True),
        ),
    ]
