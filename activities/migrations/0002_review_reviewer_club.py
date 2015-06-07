# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20150606_1327'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='reviewer_club',
            field=models.ForeignKey(related_name='reviews', verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0645\u0631\u0627\u062c\u0650\u0639', to='clubs.Club', null=True),
            preserve_default=True,
        ),
    ]
