# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_commonprofile_canceled_twitter_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonprofile',
            name='affiliation',
            field=models.CharField(default=b'', max_length=30, verbose_name='\u062c\u0647\u0629 \u0627\u0644\u062f\u0631\u0627\u0633\u0629 / \u0627\u0644\u0639\u0645\u0644'),
        ),
        migrations.AddField(
            model_name='commonprofile',
            name='gender',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u062f\u0631', choices=[(b'F', '\u0623\u0646\u062b\u0649'), (b'M', '\u0630\u0643\u0631')]),
        ),
        migrations.AddField(
            model_name='commonprofile',
            name='profile_type',
            field=models.CharField(default=b'S', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', choices=[(b'S', '\u0637\u0627\u0644\u0628\u0640/\u0640\u0629'), (b'E', '\u0645\u0648\u0638\u0641\u0640/\u0640\u0629'), (b'N', '\u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629')]),
        ),
        migrations.AlterField(
            model_name='commonprofile',
            name='city',
            field=models.CharField(default='\u0627\u0644\u0631\u064a\u0627\u0636', max_length=20, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629'),
        ),
    ]
