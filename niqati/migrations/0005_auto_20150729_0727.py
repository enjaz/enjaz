# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0004_code_order_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='category',
            field=models.ForeignKey(blank=True, to='niqati.Category', null=True),
        ),
    ]
