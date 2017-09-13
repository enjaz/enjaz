# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0007_depositoryitemrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityrequest',
            name='category',
            field=models.ForeignKey(related_name='activity_requests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641', to='activities.Category', null=True),
        ),
    ]
