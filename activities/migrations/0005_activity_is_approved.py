# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_manytomany_not_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='is_approved',
            field=models.NullBooleanField(verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(True, '\u0645\u0639\u062a\u0645\u062f'), (False, '\u0645\u0631\u0641\u0648\u0636'), (None, '\u0645\u0639\u0644\u0642')]),
        ),
    ]
