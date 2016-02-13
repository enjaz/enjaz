# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_club(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    mishkat = Club.objects.get(english_name='Mishkat', gender='F',
                               year=year_2015_2016)
    Club.objects.create(english_name="ResearchHub",
                        name="ResearchHub",
                        gender="",
                        year=year_2015_2016,
                        parent=mishkat,
                        email="researchhub@enjazportal.com",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

def remove_club(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_name="ResearchHub",
                        year=year_2015_2016).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0001_initial'),
        ('clubs', '0041_rename_to_miskhat')
    ]

    operations = [
       migrations.RunPython(
            add_club,
            reverse_code=remove_club),
    ]
