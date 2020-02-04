# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('science_olympiad', '0003_add_choice_letter'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestanswer',
            name='is_excludable',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u064a\u0645\u0643\u0646 \u062d\u0630\u0641 \u0627\u0644\u062c\u0648\u0627\u0628\u061f'),
        ),
        migrations.AddField(
            model_name='contestquestion',
            name='is_extra',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u0633\u0624\u0627\u0644 \u0625\u0636\u0627\u0641\u064a\u061f'),
        ),
        migrations.AddField(
            model_name='contestquestion',
            name='is_last_main',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0647\u0648 \u0627\u0644\u0633\u0624\u0627\u0644 \u0627\u0644\u0623\u062e\u064a\u0631 \u0645\u0646 \u0627\u0644\u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0623\u0633\u0627\u0633\u064a\u0629\u061f'),
        ),
    ]
