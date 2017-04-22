# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0052_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionregistration',
            name='is_approved',
            field=models.NullBooleanField(default=None, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(True, '\u0645\u0639\u062a\u0645\u062f'), (False, '\u0644\u0645 \u062a\u0639\u062f \u0627\u0644\u0645\u0642\u0627\u0639\u062f \u0645\u062a\u0648\u0641\u0651\u0631\u0629'), (None, '\u0645\u0639\u0644\u0642')]),
        ),
    ]
