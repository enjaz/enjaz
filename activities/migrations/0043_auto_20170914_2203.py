# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0042_activity_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='organizers',
            field=models.IntegerField(help_text='\u0639\u062f\u062f \u0627\u0644\u0637\u0644\u0627\u0628 \u0627\u0644\u0630\u064a\u0646 \u0633\u064a\u0646\u0638\u0645\u0648\u0646 \u0627\u0644\u0646\u0634\u0627\u0637', null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='participants',
            field=models.IntegerField(help_text='\u0627\u0644\u0639\u062f\u062f \u0627\u0644\u0645\u062a\u0648\u0642\u0639 \u0644\u0644\u0645\u0633\u062a\u0641\u064a\u062f\u064a\u0646 \u0645\u0646 \u0627\u0644\u0646\u0634\u0627\u0637', null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646'),
        ),
    ]
