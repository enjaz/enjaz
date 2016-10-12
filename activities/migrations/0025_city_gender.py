# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0024_null_publication_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='city',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', blank=True, choices=[(b'R', '\u0627\u0644\u0631\u064a\u0627\u0636'), (b'J', '\u062c\u062f\u0629'), (b'A', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')]),
        ),
        migrations.AddField(
            model_name='invitation',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u062f\u0631', blank=True, choices=[(b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')]),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'invitations/logos/', blank=True),
        ),
    ]
