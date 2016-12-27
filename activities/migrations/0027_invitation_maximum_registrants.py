# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0026_invitation_twitter_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='maximum_registrants',
            field=models.PositiveIntegerField(null=True, verbose_name='\u0623\u0642\u0635\u0649 \u0639\u062f\u062f \u0644\u0644\u0645\u0633\u062c\u0644\u064a\u0646 \u0648\u0627\u0644\u0645\u0633\u062c\u0644\u0627\u062a', blank=True),
        ),
    ]
