# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_old_profiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonprofile',
            name='badge_number',
            field=models.IntegerField(null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u0628\u0637\u0627\u0642\u0629 \u0627\u0644\u062c\u0627\u0645\u0639\u064a\u0629'),
        ),
    ]
