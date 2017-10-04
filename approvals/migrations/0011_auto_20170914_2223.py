# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0010_auto_20170914_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityrequest',
            name='activity',
            field=models.ForeignKey(related_name='activity_requests', verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', blank=True, to='activities.Activity', null=True),
        ),
    ]
