# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(default=b'S', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0633\u0624\u0627\u0644', choices=[(b'F', '\u0623\u0631\u0628\u0639 \u0635\u0648\u0631'), (b'Q', '\u0633\u0624\u0627\u0644'), (b'S', '\u0644\u0642\u0637\u0629')]),
        ),
    ]
