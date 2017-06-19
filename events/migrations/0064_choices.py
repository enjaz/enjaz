# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0063_is_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyquestion',
            name='choices',
            field=models.TextField(default="", help_text='\u0643\u0644 \u062e\u064a\u0627\u0631 \u0641\u064a \u0633\u0637\u0631', verbose_name='\u0627\u0644\u062e\u064a\u0627\u0631\u0627\u062a', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='surveyquestion',
            name='category',
            field=models.CharField(max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0633\u0624\u0627\u0644', choices=[(b'O', '\u0633\u0624\u0627\u0644 \u0645\u0641\u062a\u0648\u062d'), (b'C', '\u062e\u064a\u0627\u0631\u0627\u062a'), (b'I', '\u062c\u0648\u0627\u0628 \u0642\u0635\u064a\u0631'), (b'S', '\u0645\u0642\u064a\u0627\u0633'), (b'H', '\u062a\u0631\u0648\u064a\u0633\u0629')]),
        ),
    ]
