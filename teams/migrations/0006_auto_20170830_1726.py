# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_change_model_name_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='category',
            field=models.CharField(max_length=2, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0641\u0631\u064a\u0642', choices=[(b'CC', '\u0646\u0627\u062f\u064a \u0643\u0644\u064a\u0629'), (b'SC', '\u0646\u0627\u062f\u064a \u0645\u062a\u062e\u0635\u0635'), (b'I', '\u0645\u0628\u0627\u062f\u0631\u0629'), (b'P', '\u0628\u0631\u0646\u0627\u0645\u062c \u0639\u0627\u0645'), (b'CD', '\u0639\u0645\u0627\u062f\u0629 \u0643\u0644\u064a\u0629'), (b'SA', '\u0639\u0645\u0627\u062f\u0629 \u0634\u0624\u0648\u0646 \u0627\u0644\u0637\u0644\u0627\u0628'), (b'P', '\u0631\u0626\u0627\u0633\u0629 \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628')]),
        ),
    ]
