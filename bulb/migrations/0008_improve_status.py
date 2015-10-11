# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0007_readerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629 \u0627\u0644\u0639\u0627\u0645\u0629', blank=True, choices=[(b'', '\u0645\u0639\u0644\u0642\u0629'), (b'D', '\u062a\u0645'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649')]),
        ),
        migrations.AlterField(
            model_name='request',
            name='owner_status',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u062d\u0627\u0644\u0629 \u0635\u0627\u062d\u0628 \u0627\u0644\u0643\u062a\u0627\u0628', blank=True, choices=[(b'', '\u0645\u0639\u0644\u0642\u0629'), (b'D', '\u062a\u0645'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649')]),
        ),
        migrations.AlterField(
            model_name='request',
            name='requester_status',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u062d\u0627\u0644\u0629 \u0645\u0642\u062f\u0645 \u0627\u0644\u0637\u0644\u0628', blank=True, choices=[(b'', '\u0645\u0639\u0644\u0642\u0629'), (b'D', '\u062a\u0645'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649')]),
        ),
    ]
