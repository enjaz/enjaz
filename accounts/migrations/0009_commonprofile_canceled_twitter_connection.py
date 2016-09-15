# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_commonprofile_alternative_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonprofile',
            name='canceled_twitter_connection',
            field=models.BooleanField(default=False, verbose_name='\u0623\u0644\u063a\u0649 \u0637\u0644\u0628 \u0627\u0644\u0631\u0628\u0637 \u0628\u062a\u0648\u064a\u062a\u0631\u061f'),
        ),
    ]
