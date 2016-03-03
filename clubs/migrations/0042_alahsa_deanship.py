# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_alahsa_deanship(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    alahsa_deanship = Club.objects.create(
        name="عمادة شؤون الطلاب",
        english_name="Deanship of Student Affairs",
        description="",
        year=year_2015_2016,
        email="studentsclub@ksau-hs.edu.sa",
        visible=False,
        can_review=True,
        can_view_assessments=False,
        is_assessed=False,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city="A",
        )

    Club.objects.filter(english_name="Presidency (Al-Ahsa)",
                        year=year_2015_2016).update(parent=alahsa_deanship)

def remove_alahsa_deanship(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    riyadh_presidency = Club.objects.get(english_name="Presidency",
                                       year=year_2015_2016,
                                       city="R")
    alahsa_deanship = Club.objects.get(english_name="Deanship of Student Affairs",
                                       year=year_2015_2016,
                                       city="A")
    Club.objects.filter(english_name="Presidency (Al-Ahsa)",
                        year=year_2015_2016).update(parent=riyadh_presidency)
    alahsa_deanship.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0041_rename_to_miskhat'),
    ]

    operations = [
       migrations.RunPython(
            add_alahsa_deanship,
            reverse_code=remove_alahsa_deanship),
    ]
