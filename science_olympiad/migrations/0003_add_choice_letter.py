# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('science_olympiad', '0002_auto_20200131_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestanswer',
            name='choice_letter',
            field=models.CharField(default='', max_length=1, verbose_name='\u062d\u0631\u0641 \u0627\u0644\u062e\u064a\u0627\u0631', choices=[('a', '\u0623'), ('b', '\u0628'), ('c', '\u062c'), ('d', '\u062f')]),
        ),
    ]
