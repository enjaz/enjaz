# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0062_question_textarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyquestion',
            name='is_optional',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u0633\u0624\u0627\u0644 \u0627\u062e\u062a\u064a\u0627\u0631\u064a\u061f'),
        ),
        migrations.AlterField(
            model_name='surveyquestion',
            name='category',
            field=models.CharField(max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0633\u0624\u0627\u0644', choices=[(b'O', '\u0633\u0624\u0627\u0644 \u0645\u0641\u062a\u0648\u062d'), (b'S', '\u0645\u0642\u064a\u0627\u0633'), (b'H', '\u062a\u0631\u0648\u064a\u0633\u0629')]),
        ),
        migrations.AlterField(
            model_name='surveyquestion',
            name='is_english',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u0633\u0624\u0627\u0644 \u0625\u0646\u062c\u0644\u064a\u0632\u064a\u061f'),
        ),
    ]
