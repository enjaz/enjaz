# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_modify_CaseReport'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='presentaion_date',
            field=models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0639\u0631\u0636'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='presentaion_date',
            field=models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0639\u0631\u0636'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd8\xb3\xd8\xa7\xd8\xa6\xd9\x84', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
