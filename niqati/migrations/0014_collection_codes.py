# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0013_notnull_short_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='codes',
            field=models.ManyToManyField(related_name='containing_collections', to='niqati.Code', blank=True),
        ),
    ]
