# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0017_add_media_criteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='city',
            field=models.CharField(default=b'RAJ', max_length=10, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629'),
        ),
    ]
