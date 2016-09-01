# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0020_modify_citeria'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='goals',
            field=models.TextField(verbose_name='\u0645\u0627 \u0623\u0647\u062f\u0627\u0641 \u0647\u0630\u0627 \u0627\u0644\u0646\u0634\u0627\u0637\u060c \u0648\u0643\u064a\u0641 \u064a\u062e\u062f\u0645 \u0627\u0644\u0635\u0627\u0644\u062d \u0627\u0644\u0639\u0627\u0645\u061f'),
        ),
        migrations.AddField(
            model_name='review',
            name='goal_notes',
            field=models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u0623\u0647\u062f\u0627\u0641', blank=True),
        ),
    ]
