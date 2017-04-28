# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0048_improve_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', choices=[('\u0627\u0644\u0631\u064a\u0627\u0636', '\u0627\u0644\u0631\u064a\u0627\u0636'), ('\u062c\u062f\u0629', '\u062c\u062f\u0629'), ('\u0627\u0644\u0623\u062d\u0633\u0627\u0621', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')]),
        ),
    ]
