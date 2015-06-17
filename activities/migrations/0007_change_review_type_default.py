# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_activity_assignee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_type',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629', choices=[(b'P', '\u0631\u0626\u0627\u0633\u0629 \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628'), (b'D', '\u0639\u0645\u0627\u062f\u0629 \u0634\u0624\u0648\u0646 \u0627\u0644\u0637\u0644\u0627\u0628')]),
        ),
    ]
