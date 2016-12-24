# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonprofile',
            name='college_name',
            field=models.CharField(default='', max_length=30, verbose_name='\u062c\u0647\u0629 \u0627\u0644\u062f\u0631\u0627\u0633\u0629 / \u0627\u0644\u0639\u0645\u0644'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commonprofile',
            name='nonuser_city',
            field=models.TextField(verbose_name=' \u0627\u0644\u0645\u062f\u064a\u0646\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='commonprofile',
            name='profile_type',
            field=models.CharField(default=b'S', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', choices=[(b'S', '\u0637\u0627\u0644\u0628'), (b'E', '\u0645\u0648\u0638\u0641'), (b'N', '\u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629')]),
        ),
    ]
