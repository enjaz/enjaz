# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    alahsa_presidency = Club.objects.get(english_name="Presidency",
                                         year=year_2016_2017, gender="",
                                         city="A")
    jeddah_presidency = Club.objects.get(english_name="Presidency",
                                         year=year_2016_2017, gender="",
                                         city="J")

    Club.objects.create(english_name="Bulb",
                        name="سراج",
                        gender="",
                        year=year_2016_2017,
                        parent=jeddah_presidency,
                        email="bulb@enjazportal.com",
                        city="J",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    Club.objects.create(english_name="Bulb",
                        name="سراج",
                        gender="",
                        year=year_2016_2017,
                        parent=alahsa_presidency,
                        email="bulb@enjazportal.com",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    Club.objects.filter(english_name="Bulb", city__in=['J', 'A'],
                        year=year_2016_2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0018_bulb_2017_improvements'),
        ('clubs', '0046_add_jeddah_ams_deanship'),
    ]

    operations = [
       migrations.RunPython(
            add_clubs,
            reverse_code=remove_clubs),
    ]
