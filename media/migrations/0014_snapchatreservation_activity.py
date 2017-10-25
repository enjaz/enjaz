# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0041_add_jeddah_criteria'),
        ('media', '0013_auto_20170930_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapchatreservation',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='activities.Activity', null=True),
        ),
    ]
