# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fill_gender(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015, end_date__year=2016)
    m_presidency = Club.objects.filter(english_name="Presidency (Riyadh/Male)", year=year2015_2016).update(gender='M')
    f_presidency = Club.objects.filter(english_name="Presidency (Riyadh/Female)", year=year2015_2016).update(gender='F')

def empty_gender(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015, end_date__year=2016)
    m_f_presidency = Club.objects.filter(english_name__startswith="Presidency (Riyadh/", year=year2015_2016).update(gender='')

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0028_male_female_riyadh_media_center'),
    ]

    operations = [
        migrations.RunPython(
            fill_gender,
            reverse_code=empty_gender),

    ]
