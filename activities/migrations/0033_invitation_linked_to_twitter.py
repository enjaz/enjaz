# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0032_invitation_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='linked_to_twitter',
            field=models.BooleanField(default=True, verbose_name='\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u0631\u0628\u0637 \u0628\u062a\u0648\u064a\u062a\u0631'),
        ),
    ]
