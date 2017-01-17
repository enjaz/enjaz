# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0033_add notes field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='notes',
            field=models.TextField(null=True, verbose_name='\u0627\u0644\u0645\u0644\u0627\u062d\u0638\u0627\u062a', blank=True),
        ),
    ]
