# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0024_add_readathon'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcommitment',
            name='completed_pages',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='\u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0643\u062a\u0627\u0628 \u0627\u0644\u0645\u0643\u062a\u0645\u0644\u0629'),
        ),
        migrations.AddField(
            model_name='bookcommitment',
            name='pages',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='\u0635\u0641\u062d\u0627\u062a \u0627\u0644\u0643\u062a\u0627\u0628'),
        ),
    ]
