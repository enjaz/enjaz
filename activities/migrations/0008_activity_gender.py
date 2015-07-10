# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_change_review_type_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637 \u0645\u0648\u062c\u0647 \u0644', choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0627\u0644\u0637\u0644\u0627\u0628')]),
        ),
    ]
