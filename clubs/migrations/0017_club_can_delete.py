# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def deanship_cannot_delete(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015, end_date__year=2016)
    deanship = Club.objects.get(english_name="Deanship of Student Affairs", year=year2015_2016)
    deanship.can_delete = False
    deanship.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0016_separate_presidency'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='can_delete',
            field=models.BooleanField(default=True, verbose_name='\u064a\u0633\u062a\u0637\u064a\u0639 \u0627\u0644\u062d\u0630\u0641\u061f'),
        ),
       migrations.RunPython(
            deanship_cannot_delete),
    ]
