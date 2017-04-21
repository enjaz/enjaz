# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_Disscution Optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonprofile',
            name='scfhs_number',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='SCFHS Registration Number', blank=True),
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
