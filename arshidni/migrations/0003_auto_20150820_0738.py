# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_studentclubyear_niqati_closure_date'),
        ('arshidni', '0002_manytomany_not_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='colleagueprofile',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, verbose_name='\u0627\u0644\u0633\u0646\u0629', to='core.StudentClubYear', null=True),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, verbose_name='\u0627\u0644\u0633\u0646\u0629', to='core.StudentClubYear', null=True),
        ),
    ]
