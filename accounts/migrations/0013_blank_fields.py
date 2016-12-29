# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonprofile',
            name='affiliation',
            field=models.CharField(default=b'', max_length=30, verbose_name='\u062c\u0647\u0629 \u0627\u0644\u062f\u0631\u0627\u0633\u0629 / \u0627\u0644\u0639\u0645\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='commonprofile',
            name='badge_number',
            field=models.IntegerField(null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u0628\u0637\u0627\u0642\u0629 \u0627\u0644\u062c\u0627\u0645\u0639\u064a\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='commonprofile',
            name='mobile_number',
            field=models.CharField(max_length=20, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='commonprofile',
            name='user',
            field=models.OneToOneField(related_name='common_profile', verbose_name='\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='enjazprofile',
            name='user',
            field=models.OneToOneField(related_name='enjaz_profile', verbose_name='\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL),
        ),
    ]
