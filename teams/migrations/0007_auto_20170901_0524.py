# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20170828_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='position',
            field=models.CharField(default=b'M', max_length=2, verbose_name='\u0644\u0645\u0646\u0635\u0628', choices=[(b'L', '\u0645\u0645\u062b\u0644\u0640/\u0640\u0629 \u0627\u0644\u0641\u0631\u064a\u0642'), (b'VL', '\u0646\u0627\u0626\u0628 \u0645\u0645\u062b\u0644\u0640/\u0640\u0629 \u0627\u0644\u0641\u0631\u064a\u0642'), (b'SR', '\u0627\u0644\u0645\u0645\u062b\u0644\u0640/\u0640\u0629 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a\u0640/\u0640\u0629 \u0644\u0644\u0641\u0631\u064a\u0642'), (b'AM', '\u0639\u0636\u0648/\u0629 \u0641\u0639\u0627\u0644\u0640/\u0640\u0629'), (b'M', '\u0639\u0636\u0648/\u0629')]),
        ),
    ]
