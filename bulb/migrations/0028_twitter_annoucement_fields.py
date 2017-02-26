# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0027_readathon_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='featured_announcement_date',
            field=models.DateField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0639\u0644\u0627\u0646'),
        ),
        migrations.AddField(
            model_name='book',
            name='is_featured',
            field=models.NullBooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u0643\u062a\u0627\u0628 \u0645\u062e\u062a\u0627\u0631\u061f'),
        ),
        migrations.AddField(
            model_name='book',
            name='was_announced',
            field=models.NullBooleanField(default=False, verbose_name='\u0623\u0639\u0644\u0646 \u0639\u0646\u0647\u061f'),
        ),
    ]
