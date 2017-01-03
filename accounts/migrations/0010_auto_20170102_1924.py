# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_commonprofile_canceled_twitter_connection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonprofile',
            name='user',
            field=models.OneToOneField(related_name='common_profile', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='enjazprofile',
            name='user',
            field=models.OneToOneField(related_name='enjaz_profile', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
