# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_years'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentclubyear',
            name='niqati_closure_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u063a\u0644\u0627\u0642 \u0646\u0642\u0627\u0637\u064a', blank=True),
        ),
    ]
