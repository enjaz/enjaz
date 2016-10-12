# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0023_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='full_description',
            field=models.TextField(verbose_name='\u0648\u0635\u0641 \u0645\u0637\u0648\u0644'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='publication_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0634\u0631', blank=True),
        ),
    ]
