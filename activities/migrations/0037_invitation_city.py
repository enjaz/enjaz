# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0036_invitation_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='city',
            field=models.CharField(default=b'', max_length=20, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', blank=True, choices=[('\u0627\u0644\u0631\u064a\u0627\u0636', '\u0627\u0644\u0631\u064a\u0627\u0636'), ('\u062c\u062f\u0629', '\u062c\u062f\u0629'), ('\u0627\u0644\u0623\u062d\u0633\u0627\u0621', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')]),
        ),
    ]
