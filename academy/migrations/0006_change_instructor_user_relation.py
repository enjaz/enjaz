# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0005_Temporary_Stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL),
        ),
    ]
